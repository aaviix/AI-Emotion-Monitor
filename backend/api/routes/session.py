"""
Session management API endpoints.

Provides endpoints for:
- Creating new clinical sessions
- Ending sessions
- Getting session details
- Updating calibration settings
"""

from flask import Blueprint, request, jsonify

from backend.services.session_manager import session_manager
from backend.core.inference import CalibrationSettings


bp = Blueprint('session', __name__)


@bp.route('/start', methods=['POST'])
def start_session():
    """
    Start a new clinical monitoring session.

    Request (application/json - optional):
        {
            "calibration": {
                "sad_boost": 2.5,
                "anger_boost": 2.0,
                "neutral_suppress": 0.3
            }
        }

    Response:
        {
            "session_id": "uuid-string",
            "start_time": "2026-03-16T12:00:00",
            "calibration": {...},
            "is_active": true
        }
    """
    try:
        # Parse optional calibration settings
        calibration = None
        if request.json and 'calibration' in request.json:
            cal_data = request.json['calibration']
            calibration = CalibrationSettings(
                sad_boost=cal_data.get('sad_boost', 2.5),
                anger_boost=cal_data.get('anger_boost', 2.0),
                neutral_suppress=cal_data.get('neutral_suppress', 0.3)
            )

        # Create session
        session = session_manager.create_session(calibration=calibration)

        return jsonify(session.to_dict()), 201

    except RuntimeError as e:
        return jsonify({'error': str(e)}), 429  # Too many sessions
    except Exception as e:
        return jsonify({'error': f'Failed to create session: {str(e)}'}), 500


@bp.route('/stop/<session_id>', methods=['POST'])
def stop_session(session_id: str):
    """
    End an active session.

    Response:
        {
            "session_id": "uuid-string",
            "start_time": "2026-03-16T12:00:00",
            "end_time": "2026-03-16T12:10:00",
            "duration_seconds": 600.0,
            "num_frames": 3000,
            "is_active": false
        }
    """
    try:
        session = session_manager.end_session(session_id)

        if session is None:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        return jsonify(session.to_dict()), 200

    except Exception as e:
        return jsonify({'error': f'Failed to end session: {str(e)}'}), 500


@bp.route('/<session_id>', methods=['GET'])
def get_session(session_id: str):
    """
    Get session details.

    Response:
        {
            "session_id": "uuid-string",
            "start_time": "2026-03-16T12:00:00",
            "end_time": null,
            "duration_seconds": 120.5,
            "calibration": {...},
            "num_frames": 600,
            "is_active": true
        }
    """
    try:
        session = session_manager.get_session(session_id)

        if session is None:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        return jsonify(session.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<session_id>/calibration', methods=['PUT'])
def update_calibration(session_id: str):
    """
    Update calibration settings for a session.

    Request (application/json):
        {
            "sad_boost": 3.0,
            "anger_boost": 2.5,
            "neutral_suppress": 0.4
        }

    Response:
        {
            "session_id": "uuid-string",
            "calibration": {...}
        }
    """
    try:
        if not request.json:
            return jsonify({'error': 'Request body must be JSON'}), 400

        # Parse calibration settings
        calibration = CalibrationSettings(
            sad_boost=request.json.get('sad_boost', 2.5),
            anger_boost=request.json.get('anger_boost', 2.0),
            neutral_suppress=request.json.get('neutral_suppress', 0.3)
        )

        # Update session
        success = session_manager.update_calibration(session_id, calibration)

        if not success:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        return jsonify({
            'session_id': session_id,
            'calibration': {
                'sad_boost': calibration.sad_boost,
                'anger_boost': calibration.anger_boost,
                'neutral_suppress': calibration.neutral_suppress
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to update calibration: {str(e)}'}), 500


@bp.route('/active', methods=['GET'])
def get_active_sessions():
    """
    Get all active sessions.

    Response:
        {
            "sessions": [
                {"session_id": "...", "start_time": "...", ...},
                ...
            ],
            "count": 2
        }
    """
    try:
        sessions = session_manager.get_active_sessions()
        return jsonify({
            'sessions': [s.to_dict() for s in sessions],
            'count': len(sessions)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<session_id>', methods=['DELETE'])
def delete_session(session_id: str):
    """
    Delete a session permanently.

    Response:
        {
            "message": "Session deleted successfully"
        }
    """
    try:
        success = session_manager.delete_session(session_id)

        if not success:
            return jsonify({'error': f'Session {session_id} not found'}), 404

        return jsonify({'message': 'Session deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
