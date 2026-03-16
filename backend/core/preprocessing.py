"""
Image preprocessing utilities for emotion detection.

This module provides functions for facial image preprocessing including:
- CLAHE (Contrast Limited Adaptive Histogram Equalization) for lighting normalization
- Haar Cascade face detection
- Image transformations for model input (48x48 grayscale, normalization)

These preprocessing steps are critical for "clinical-ready" emotion detection,
especially in environments with poor lighting conditions (e.g., yellow clinical lights).
"""

import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from typing import List, Tuple, Optional


# Global transform pipeline for FER2013 model input
# FER2013 uses 48x48 grayscale images with 0-1 normalization
EMOTION_TRANSFORM = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),  # Converts to [0, 1] range
])


class FaceDetector:
    """
    Haar Cascade-based face detector for real-time facial region extraction.

    Uses OpenCV's pre-trained Haar Cascade classifier to detect frontal faces.
    """

    def __init__(self):
        """Initialize Haar Cascade face detector."""
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            raise RuntimeError(f"Failed to load Haar Cascade from {cascade_path}")

    def detect_faces(
        self,
        gray_frame: np.ndarray,
        scale_factor: float = 1.1,
        min_neighbors: int = 7,
        min_size: Tuple[int, int] = (60, 60)
    ) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in a grayscale image.

        Args:
            gray_frame (np.ndarray): Grayscale image (H, W)
            scale_factor (float): How much the image size is reduced at each scale
            min_neighbors (int): Min neighbors for detection (higher = fewer false positives)
            min_size (Tuple[int, int]): Minimum face size (width, height)

        Returns:
            List[Tuple[int, int, int, int]]: List of detected faces as (x, y, w, h) tuples
        """
        faces = self.face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size
        )

        # Convert numpy array to list of tuples
        return [tuple(face) for face in faces]


class CLAHEProcessor:
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) processor.

    CLAHE enhances contrast in images while avoiding over-amplification of noise.
    Essential for handling poor clinical lighting conditions that can obscure micro-expressions.
    """

    def __init__(self, clip_limit: float = 2.0, tile_grid_size: Tuple[int, int] = (8, 8)):
        """
        Initialize CLAHE processor.

        Args:
            clip_limit (float): Threshold for contrast limiting (default: 2.0)
            tile_grid_size (Tuple[int, int]): Size of grid for histogram equalization (default: 8x8)
        """
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    def apply(self, gray_image: np.ndarray) -> np.ndarray:
        """
        Apply CLAHE to a grayscale image.

        Args:
            gray_image (np.ndarray): Grayscale image (H, W)

        Returns:
            np.ndarray: CLAHE-enhanced grayscale image
        """
        return self.clahe.apply(gray_image)


def preprocess_face_for_model(
    face_roi: np.ndarray,
    apply_clahe: bool = True,
    clahe_processor: Optional[CLAHEProcessor] = None
) -> 'torch.Tensor':
    """
    Preprocess a face ROI for emotion model inference.

    Args:
        face_roi (np.ndarray): Grayscale face region of interest
        apply_clahe (bool): Whether to apply CLAHE preprocessing (default: True)
        clahe_processor (Optional[CLAHEProcessor]): CLAHE processor instance (creates new if None)

    Returns:
        torch.Tensor: Preprocessed tensor of shape (1, 1, 48, 48) ready for model input
    """
    if face_roi.size == 0:
        raise ValueError("Face ROI is empty")

    # Apply CLAHE if requested
    if apply_clahe:
        if clahe_processor is None:
            clahe_processor = CLAHEProcessor()
        face_roi = clahe_processor.apply(face_roi)

    # Convert numpy array to PIL Image
    pil_img = Image.fromarray(face_roi)

    # Apply transforms: grayscale -> resize to 48x48 -> normalize to [0, 1]
    tensor = EMOTION_TRANSFORM(pil_img).unsqueeze(0)  # Add batch dimension

    return tensor


def convert_to_grayscale(frame: np.ndarray) -> np.ndarray:
    """
    Convert BGR image to grayscale.

    Args:
        frame (np.ndarray): BGR image (H, W, 3)

    Returns:
        np.ndarray: Grayscale image (H, W)
    """
    if len(frame.shape) == 2:
        # Already grayscale
        return frame
    elif frame.shape[2] == 3:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif frame.shape[2] == 4:
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    else:
        raise ValueError(f"Unsupported image shape: {frame.shape}")


def draw_face_detection(
    frame: np.ndarray,
    face_bbox: Tuple[int, int, int, int],
    emotion_label: str,
    confidence: float,
    color: Tuple[int, int, int] = (0, 255, 0)
) -> np.ndarray:
    """
    Draw face bounding box and emotion label on image.

    Args:
        frame (np.ndarray): Image to draw on (BGR format)
        face_bbox (Tuple[int, int, int, int]): Face bounding box (x, y, w, h)
        emotion_label (str): Emotion label to display
        confidence (float): Confidence score (0-1)
        color (Tuple[int, int, int]): BGR color for rectangle and text (default: green)

    Returns:
        np.ndarray: Image with drawn annotations
    """
    x, y, w, h = face_bbox

    # Draw rectangle around face
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Draw emotion label with confidence
    label_text = f"{emotion_label}: {confidence:.1%}"
    cv2.putText(
        frame,
        label_text,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )

    return frame
