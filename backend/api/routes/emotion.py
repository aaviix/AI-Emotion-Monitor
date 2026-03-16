"""
Emotion detection API endpoints.

Provides endpoints for:
- Single frame emotion detection
- Real-time video stream emotion processing (client-push model)
"""

from flask import Blueprint, request, jsonify, current_app
import cv2
import numpy as np
import base64
from typing import Optional

from backend.services.session_manager import session_manager


bp = Blueprint('emotion', __name__)


def get_inference_engine():
    """Get the inference engine from the active Flask app context."""
    inference_engine = current_app.extensions.get('inference_engine')
    if inference_engine is None:
        raise RuntimeError('Inference engine not initialized')
    return inference_engine


def to_json_safe(value):
    """Recursively convert NumPy values to JSON-serializable Python types."""
    if isinstance(value, dict):
        return {key: to_json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_json_safe(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


def decode_image_from_request(request_data) -> Optional[np.ndarray]:
    """
    Decode image from request (multipart file or base64).

    Args:
        request_data: Flask request object

    Returns:
        Optional[np.ndarray]: Decoded image (BGR format) or None if error
    """
    try:
        # Try multipart file upload first
        if 'file' in request.files:
            file = request.files['file']
            file_bytes = np.frombuffer(file.read(), np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            return frame

        # Try base64 encoded image
        elif 'image' in request.json:
            image_b64 = request.json['image']

            # Remove data URL prefix if present (e.g., "data:image/jpeg;base64,")
            if ',' in image_b64:
                image_b64 = image_b64.split(',')[1]

            # Decode base64
            image_bytes = base64.b64decode(image_b64)
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return frame

        else:
            return None

    except Exception as e:
        print(f"Error decoding image: {e}")
        return None


@bp.route('/detect', methods=['POST'])
def detect_emotion():
    """
    Detect emotions in a single frame.

    Request (multipart/form-data):
        - file: Image file

    OR Request (application/json):
        - image: base64 encoded image

    Response:
        {
            "emotion_probs": {"Angry": 0.1, "Happy": 0.8, ...},
            "dominant_emotion": "Happy",
            "confidence": 0.8,
            "faces": [[x, y, w, h], ...],
            "num_faces": 1
        }
    """
    try:
        # Decode image from request
        frame = decode_image_from_request(request)
        if frame is None:
            return jsonify({'error': 'Invalid image data. Provide file or base64 image.'}), 400

        # Get inference engine
        engine = get_inference_engine()

        # Run emotion detection
        result = engine.detect_emotion(frame, apply_clahe=True)

        # Format response
        response = {
            'emotion_probs': result.emotion_probs,
            'dominant_emotion': result.dominant_emotion,
            'confidence': result.confidence,
            'faces': [list(face) for face in result.faces],
            'num_faces': len(result.faces)
        }

        return jsonify(to_json_safe(response)), 200

    except Exception as e:
        return jsonify({'error': f'Emotion detection failed: {str(e)}'}), 500


@bp.route('/stream', methods=['POST'])
def stream_emotion():
    """
    Process video stream frame with session-specific temporal smoothing.

    Request (application/json):
        - image: base64 encoded frame
        - session_id: Session UUID
        - apply_calibration: (optional) Whether to apply calibration (default: true)

    Response:
        {
            "emotion_probs": {"Angry": 0.1, "Happy": 0.8, ...},
            "dominant_emotion": "Happy",
            "confidence": 0.8,
            "faces": [[x, y, w, h], ...],
            "num_faces": 1,
            "timestamp": 12.5  # Elapsed session time in seconds
        }
    """
    try:
        # Parse request
        data = request.json
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        session_id = data.get('session_id')
        if not session_id:
            return jsonify({'error': 'session_id is required'}), 400

        # Get session
        session = session_manager.get_session(session_id)
        if not session:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        if not session.is_active:
            return jsonify({'error': f'Session {session_id} is not active'}), 400

        # Decode image
        frame = decode_image_from_request(request)
        if frame is None:
            return jsonify({'error': 'Invalid image data. Provide base64 image.'}), 400

        # Get inference engine and update calibration if needed
        engine = get_inference_engine()
        engine.update_calibration(session.calibration)

        # Run emotion detection (smoothing is handled per-engine, not per-session currently)
        # Note: For true per-session smoothing, we'd need separate buffers per session
        result = engine.detect_emotion(frame, apply_clahe=True)

        # Add emotion data to session
        session_manager.add_emotion_data(session_id, result.emotion_probs)

        # Format response
        response = {
            'emotion_probs': result.emotion_probs,
            'dominant_emotion': result.dominant_emotion,
            'confidence': result.confidence,
            'faces': [list(face) for face in result.faces],
            'num_faces': len(result.faces),
            'timestamp': session.get_duration()
        }

        return jsonify(to_json_safe(response)), 200

    except Exception as e:
        return jsonify({'error': f'Stream processing failed: {str(e)}'}), 500


@bp.route('/emotions', methods=['GET'])
def get_emotion_labels():
    """
    Get the list of emotion labels.

    Response:
        {
            "emotions": ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
        }
    """
    try:
        engine = get_inference_engine()
        return jsonify({'emotions': engine.get_emotion_labels()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
