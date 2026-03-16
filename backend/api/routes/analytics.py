"""
Analytics API endpoints.

Provides endpoints for:
- Clinical assessment generation
- Time-series emotion data
- Session statistics
"""

from flask import Blueprint, request, jsonify

from backend.services.session_manager import session_manager
from backend.services import analytics_engine


bp = Blueprint('analytics', __name__)


@bp.route('/summary/<session_id>', methods=['GET'])
def get_summary(session_id: str):
    """
    Get clinical assessment summary for a session.

    Response:
        {
            "session_id": "uuid-string",
            "duration_seconds": 600.0,
            "num_frames": 3000,
            "avg_emotions": {
                "Angry": 0.05,
                "Happy": 0.35,
                ...
            },
            "distress_score": 0.25,
            "stability_score": 0.65,
            "assessment": {
                "summary": "High Emotional Stability Detected (0.65)",
                "level": "success",
                "details": [...],
                "recommendations": [...]
            }
        }
    """
    try:
        # Get session
        session = session_manager.get_session(session_id)
        if session is None:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        if len(session.emotion_history) == 0:
            return jsonify({'error': 'No emotion data available for this session'}), 400

        # Calculate analytics
        avg_emotions = analytics_engine.calculate_avg_emotions(session.emotion_history)
        distress_score = analytics_engine.calculate_distress_score(avg_emotions)
        stability_score = analytics_engine.calculate_stability_score(avg_emotions)
        assessment = analytics_engine.generate_clinical_assessment(
            avg_emotions,
            distress_score,
            stability_score
        )

        # Format response
        response = {
            'session_id': session_id,
            'duration_seconds': session.get_duration(),
            'num_frames': len(session.emotion_history),
            'avg_emotions': avg_emotions,
            'distress_score': distress_score,
            'stability_score': stability_score,
            'assessment': assessment
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'Failed to generate summary: {str(e)}'}), 500


@bp.route('/timeseries/<session_id>', methods=['GET'])
def get_timeseries(session_id: str):
    """
    Get time-series emotion data for a session.

    Query parameters:
        - window_size (optional): Number of frames to average (default: 30)

    Response:
        {
            "session_id": "uuid-string",
            "timestamps": [0.0, 0.1, 0.2, ...],
            "emotions": [
                {"Angry": 0.1, "Happy": 0.5, ...},
                {"Angry": 0.08, "Happy": 0.55, ...},
                ...
            ]
        }
    """
    try:
        # Get session
        session = session_manager.get_session(session_id)
        if session is None:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        if len(session.emotion_history) == 0:
            return jsonify({'error': 'No emotion data available for this session'}), 400

        # Parse window size
        window_size = request.args.get('window_size', default=30, type=int)

        # Generate time-series data
        timeseries = analytics_engine.generate_timeseries_summary(
            session.emotion_history,
            session.timestamps,
            window_size=window_size
        )

        response = {
            'session_id': session_id,
            **timeseries
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'Failed to generate timeseries: {str(e)}'}), 500


@bp.route('/distribution/<session_id>', methods=['GET'])
def get_emotion_distribution(session_id: str):
    """
    Get emotion distribution (dominant emotion frequencies) for a session.

    Response:
        {
            "session_id": "uuid-string",
            "distribution": {
                "Happy": 1500,
                "Neutral": 1200,
                "Sad": 300,
                ...
            },
            "total_frames": 3000
        }
    """
    try:
        # Get session
        session = session_manager.get_session(session_id)
        if session is None:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        if len(session.emotion_history) == 0:
            return jsonify({'error': 'No emotion data available for this session'}), 400

        # Calculate distribution
        distribution = analytics_engine.get_emotion_distribution(session.emotion_history)

        response = {
            'session_id': session_id,
            'distribution': distribution,
            'total_frames': len(session.emotion_history)
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/variability/<session_id>', methods=['GET'])
def get_emotion_variability(session_id: str):
    """
    Get emotion variability (standard deviation) for a session.

    High variability may indicate emotional instability or reactivity.

    Response:
        {
            "session_id": "uuid-string",
            "variability": {
                "Angry": 0.05,
                "Happy": 0.12,
                ...
            }
        }
    """
    try:
        # Get session
        session = session_manager.get_session(session_id)
        if session is None:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        if len(session.emotion_history) == 0:
            return jsonify({'error': 'No emotion data available for this session'}), 400

        # Calculate variability
        variability = analytics_engine.calculate_emotion_variability(session.emotion_history)

        response = {
            'session_id': session_id,
            'variability': variability
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
