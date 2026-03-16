"""
Emotion Inference Engine for real-time emotion detection.

This module provides the EmotionInferenceEngine class which encapsulates:
- Model loading and caching
- Frame-by-frame emotion detection with face detection
- Temporal smoothing (deque buffer for stable predictions)
- Clinical calibration (adjustable sensitivity for specific emotions)

This is the central inference component shared by Flask API and Streamlit applications.
"""

import torch
import torch.nn as nn
import numpy as np
from collections import deque
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from backend.core.model import ImprovedCNNEmotion
from backend.core.preprocessing import (
    FaceDetector,
    CLAHEProcessor,
    preprocess_face_for_model,
    convert_to_grayscale
)


@dataclass
class EmotionResult:
    """Result from emotion detection on a single frame."""
    emotion_probs: Dict[str, float]  # Emotion probabilities
    dominant_emotion: str             # Emotion with highest probability
    confidence: float                 # Confidence of dominant emotion
    faces: List[Tuple[int, int, int, int]]  # List of detected face bounding boxes (x, y, w, h)


@dataclass
class CalibrationSettings:
    """Clinical calibration settings for emotion sensitivity adjustment."""
    sad_boost: float = 2.5             # Sensitivity multiplier for Sadness (1.0-5.0)
    anger_boost: float = 2.0           # Sensitivity multiplier for Anger (1.0-5.0)
    neutral_suppress: float = 0.3      # Suppression factor for Neutral (0.0-1.0)


class EmotionInferenceEngine:
    """
    Inference engine for real-time emotion detection from facial images.

    This class loads the ImprovedCNNEmotion model and provides methods for:
    - Single frame emotion detection
    - Temporal smoothing to prevent label "flickering"
    - Clinical calibration to adjust for individual baselines
    """

    # FER2013 emotion labels (index order must match model training)
    EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    def __init__(
        self,
        model_path: str,
        device: Optional[str] = None,
        enable_smoothing: bool = True,
        smoothing_window: int = 8,
        enable_calibration: bool = True,
        calibration_settings: Optional[CalibrationSettings] = None
    ):
        """
        Initialize the emotion inference engine.

        Args:
            model_path (str): Path to the trained model weights (.pth file)
            device (Optional[str]): Device for inference ('cuda' or 'cpu'). Auto-detects if None.
            enable_smoothing (bool): Enable temporal smoothing (default: True)
            smoothing_window (int): Size of probability buffer for smoothing (default: 8)
            enable_calibration (bool): Enable clinical calibration (default: True)
            calibration_settings (Optional[CalibrationSettings]): Calibration parameters
        """
        # Device setup
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device

        # Load model
        self.model = ImprovedCNNEmotion(num_classes=7)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        # Preprocessing components
        self.face_detector = FaceDetector()
        self.clahe_processor = CLAHEProcessor()

        # Temporal smoothing setup
        self.enable_smoothing = enable_smoothing
        self.smoothing_window = smoothing_window
        self.prob_buffer = deque(maxlen=smoothing_window)

        # Clinical calibration setup
        self.enable_calibration = enable_calibration
        self.calibration_settings = calibration_settings or CalibrationSettings()

    def detect_emotion(
        self,
        frame: np.ndarray,
        apply_clahe: bool = True,
        return_all_faces: bool = False
    ) -> EmotionResult:
        """
        Detect emotions in a single frame.

        Args:
            frame (np.ndarray): Input frame (BGR or grayscale)
            apply_clahe (bool): Apply CLAHE preprocessing (default: True)
            return_all_faces (bool): Return emotions for all faces (default: False, uses first face)

        Returns:
            EmotionResult: Emotion detection result with probabilities and face locations
        """
        # Convert to grayscale if needed
        gray_frame = convert_to_grayscale(frame)

        # Detect faces
        faces = self.face_detector.detect_faces(gray_frame)

        if len(faces) == 0:
            # No faces detected - return neutral probabilities
            return EmotionResult(
                emotion_probs={emotion: 1.0/7 for emotion in self.EMOTIONS},
                dominant_emotion='Neutral',
                confidence=1.0/7,
                faces=[]
            )

        # Process first face (or all faces if requested)
        face = faces[0]
        x, y, w, h = face
        face_roi = gray_frame[y:y+h, x:x+w]

        if face_roi.size == 0:
            return EmotionResult(
                emotion_probs={emotion: 1.0/7 for emotion in self.EMOTIONS},
                dominant_emotion='Neutral',
                confidence=1.0/7,
                faces=faces
            )

        # Preprocess face ROI
        face_tensor = preprocess_face_for_model(
            face_roi,
            apply_clahe=apply_clahe,
            clahe_processor=self.clahe_processor if apply_clahe else None
        )
        face_tensor = face_tensor.to(self.device)

        # Run inference
        with torch.no_grad():
            output = self.model(face_tensor)
            probs = torch.softmax(output, dim=1).cpu().numpy()[0]

        # Apply clinical calibration
        if self.enable_calibration:
            probs = self._apply_calibration(probs)

        # Apply temporal smoothing
        if self.enable_smoothing:
            self.prob_buffer.append(probs)
            probs = np.mean(self.prob_buffer, axis=0)

        # Create emotion probability dictionary
        emotion_probs = {emotion: float(prob) for emotion, prob in zip(self.EMOTIONS, probs)}

        # Get dominant emotion
        dominant_idx = np.argmax(probs)
        dominant_emotion = self.EMOTIONS[dominant_idx]
        confidence = float(probs[dominant_idx])

        return EmotionResult(
            emotion_probs=emotion_probs,
            dominant_emotion=dominant_emotion,
            confidence=confidence,
            faces=faces
        )

    def _apply_calibration(self, probs: np.ndarray) -> np.ndarray:
        """
        Apply clinical calibration to emotion probabilities.

        This adjusts probabilities based on calibration settings to account for:
        - Individual patient baselines
        - Environmental factors (lighting, muscle tension)
        - Clinical context

        Args:
            probs (np.ndarray): Raw emotion probabilities (7,)

        Returns:
            np.ndarray: Calibrated and re-normalized probabilities (7,)
        """
        # Create a copy to avoid modifying original
        calibrated = probs.copy()

        # Apply sensitivity boosts/suppressions
        # Index mapping: 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Neutral, 5=Sad, 6=Surprise
        calibrated[5] *= self.calibration_settings.sad_boost        # Sad
        calibrated[0] *= self.calibration_settings.anger_boost      # Angry
        calibrated[4] *= (1.0 - self.calibration_settings.neutral_suppress)  # Neutral

        # Clip to valid range and re-normalize
        calibrated = np.clip(calibrated, 0, 1)
        calibrated /= np.sum(calibrated)

        return calibrated

    def update_calibration(self, calibration_settings: CalibrationSettings):
        """
        Update clinical calibration settings.

        Args:
            calibration_settings (CalibrationSettings): New calibration parameters
        """
        self.calibration_settings = calibration_settings

    def reset_smoothing_buffer(self):
        """Reset the temporal smoothing buffer (useful when starting a new session)."""
        self.prob_buffer.clear()

    def get_emotion_index(self, emotion_name: str) -> int:
        """
        Get the index of an emotion by name.

        Args:
            emotion_name (str): Emotion name (case-sensitive)

        Returns:
            int: Index in EMOTIONS list

        Raises:
            ValueError: If emotion name is not found
        """
        try:
            return self.EMOTIONS.index(emotion_name)
        except ValueError:
            raise ValueError(f"Unknown emotion: {emotion_name}. Valid emotions: {self.EMOTIONS}")

    @classmethod
    def get_emotion_labels(cls) -> List[str]:
        """
        Get the list of emotion labels.

        Returns:
            List[str]: List of 7 emotion labels
        """
        return cls.EMOTIONS.copy()
