"""
Configuration management for AI Emotion Monitor.

This module handles loading configuration from environment variables and provides
default values for all system settings. Uses python-dotenv for .env file support.
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Application configuration loaded from environment variables.

    All settings can be overridden via environment variables or .env file.
    """

    # === Model Configuration ===
    MODEL_PATH: str = os.getenv(
        'MODEL_PATH',
        str(Path(__file__).parent.parent.parent / 'models' / 'emotion_model_cnn_improved.pth')
    )

    DEVICE: str = os.getenv('DEVICE', 'cpu')  # 'cuda' or 'cpu'

    # Emotion labels (FER2013 standard order)
    EMOTIONS: List[str] = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    # === Flask API Configuration ===
    API_HOST: str = os.getenv('API_HOST', '0.0.0.0')
    API_PORT: int = int(os.getenv('API_PORT', '5000'))
    API_DEBUG: bool = os.getenv('API_DEBUG', 'true').lower() == 'true'

    # CORS settings (comma-separated list of allowed origins)
    CORS_ORIGINS: List[str] = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # === Inference Configuration ===
    ENABLE_SMOOTHING: bool = os.getenv('ENABLE_SMOOTHING', 'true').lower() == 'true'
    SMOOTHING_WINDOW: int = int(os.getenv('SMOOTHING_WINDOW', '8'))

    ENABLE_CALIBRATION: bool = os.getenv('ENABLE_CALIBRATION', 'true').lower() == 'true'

    # === Clinical Calibration Defaults ===
    DEFAULT_SAD_BOOST: float = float(os.getenv('DEFAULT_SAD_BOOST', '2.5'))
    DEFAULT_ANGER_BOOST: float = float(os.getenv('DEFAULT_ANGER_BOOST', '2.0'))
    DEFAULT_NEUTRAL_SUPPRESS: float = float(os.getenv('DEFAULT_NEUTRAL_SUPPRESS', '0.3'))

    # === Face Detection Configuration ===
    FACE_SCALE_FACTOR: float = float(os.getenv('FACE_SCALE_FACTOR', '1.1'))
    FACE_MIN_NEIGHBORS: int = int(os.getenv('FACE_MIN_NEIGHBORS', '7'))
    FACE_MIN_SIZE: int = int(os.getenv('FACE_MIN_SIZE', '60'))  # Min size for both width and height

    # === CLAHE Configuration ===
    CLAHE_CLIP_LIMIT: float = float(os.getenv('CLAHE_CLIP_LIMIT', '2.0'))
    CLAHE_TILE_GRID_SIZE: int = int(os.getenv('CLAHE_TILE_GRID_SIZE', '8'))

    # === Session Configuration ===
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
    MAX_ACTIVE_SESSIONS: int = int(os.getenv('MAX_ACTIVE_SESSIONS', '100'))

    @classmethod
    def validate(cls):
        """
        Validate configuration settings.

        Raises:
            ValueError: If any configuration is invalid
            FileNotFoundError: If model path doesn't exist
        """
        # Check model file exists
        model_path = Path(cls.MODEL_PATH)
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {cls.MODEL_PATH}. "
                f"Please ensure the model file exists or set MODEL_PATH environment variable."
            )

        # Validate device
        if cls.DEVICE not in ['cuda', 'cpu']:
            raise ValueError(f"Invalid DEVICE: {cls.DEVICE}. Must be 'cuda' or 'cpu'.")

        # Validate numeric ranges
        if not (1.0 <= cls.DEFAULT_SAD_BOOST <= 5.0):
            raise ValueError(f"DEFAULT_SAD_BOOST must be between 1.0 and 5.0, got {cls.DEFAULT_SAD_BOOST}")

        if not (1.0 <= cls.DEFAULT_ANGER_BOOST <= 5.0):
            raise ValueError(f"DEFAULT_ANGER_BOOST must be between 1.0 and 5.0, got {cls.DEFAULT_ANGER_BOOST}")

        if not (0.0 <= cls.DEFAULT_NEUTRAL_SUPPRESS <= 1.0):
            raise ValueError(f"DEFAULT_NEUTRAL_SUPPRESS must be between 0.0 and 1.0, got {cls.DEFAULT_NEUTRAL_SUPPRESS}")

    @classmethod
    def display(cls):
        """Display current configuration (for debugging/logging)."""
        print("=" * 60)
        print("AI Emotion Monitor Configuration")
        print("=" * 60)
        print(f"Model Path:          {cls.MODEL_PATH}")
        print(f"Device:              {cls.DEVICE}")
        print(f"API Host:            {cls.API_HOST}:{cls.API_PORT}")
        print(f"API Debug:           {cls.API_DEBUG}")
        print(f"CORS Origins:        {', '.join(cls.CORS_ORIGINS)}")
        print(f"Smoothing Enabled:   {cls.ENABLE_SMOOTHING} (window={cls.SMOOTHING_WINDOW})")
        print(f"Calibration Enabled: {cls.ENABLE_CALIBRATION}")
        print(f"  - Sadness Boost:   {cls.DEFAULT_SAD_BOOST}")
        print(f"  - Anger Boost:     {cls.DEFAULT_ANGER_BOOST}")
        print(f"  - Neutral Suppress: {cls.DEFAULT_NEUTRAL_SUPPRESS}")
        print("=" * 60)


# Create a singleton instance
config = Config()


# Validate configuration on module import (optional - can remove if too strict)
# config.validate()
