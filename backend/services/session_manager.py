"""
Session management for clinical emotion monitoring sessions.

This module manages session state including:
- Session creation and destruction
- Emotion history tracking
- Calibration settings per session
- Probability buffers for temporal smoothing

For production, consider using Redis for distributed session storage.
For now, this uses in-memory storage with UUID-based session IDs.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import deque
import numpy as np

from backend.utils.config import config
from backend.core.inference import CalibrationSettings


@dataclass
class SessionData:
    """Data structure for a clinical monitoring session."""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    calibration: CalibrationSettings = field(default_factory=CalibrationSettings)
    emotion_history: List[Dict[str, float]] = field(default_factory=list)
    timestamps: List[float] = field(default_factory=list)  # Elapsed time in seconds
    prob_buffer: deque = field(default_factory=lambda: deque(maxlen=8))
    is_active: bool = True

    def get_duration(self) -> float:
        """Get session duration in seconds."""
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()

    def add_emotion_data(self, emotion_probs: Dict[str, float]):
        """Add emotion probabilities to history."""
        elapsed_time = self.get_duration()
        self.emotion_history.append(emotion_probs)
        self.timestamps.append(elapsed_time)

    def get_latest_emotions(self, count: int = 10) -> List[Dict[str, float]]:
        """Get the latest N emotion probability records."""
        return self.emotion_history[-count:]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.get_duration(),
            'is_active': self.is_active,
            'calibration': {
                'sad_boost': self.calibration.sad_boost,
                'anger_boost': self.calibration.anger_boost,
                'neutral_suppress': self.calibration.neutral_suppress
            },
            'num_frames': len(self.emotion_history)
        }


class SessionManager:
    """
    Manages clinical monitoring sessions.

    Uses in-memory storage with automatic cleanup of expired sessions.
    """

    def __init__(self):
        """Initialize session manager."""
        self._sessions: Dict[str, SessionData] = {}
        self._timeout_minutes = config.SESSION_TIMEOUT_MINUTES
        self._max_sessions = config.MAX_ACTIVE_SESSIONS

    def create_session(
        self,
        calibration: Optional[CalibrationSettings] = None
    ) -> SessionData:
        """
        Create a new clinical monitoring session.

        Args:
            calibration (Optional[CalibrationSettings]): Custom calibration settings

        Returns:
            SessionData: New session object

        Raises:
            RuntimeError: If max active sessions limit is reached
        """
        # Clean up expired sessions before creating new one
        self._cleanup_expired_sessions()

        # Check session limit
        if len(self._sessions) >= self._max_sessions:
            raise RuntimeError(
                f"Maximum active sessions ({self._max_sessions}) reached. "
                "Please end existing sessions or increase MAX_ACTIVE_SESSIONS."
            )

        # Generate unique session ID
        session_id = str(uuid.uuid4())

        # Create session with default or custom calibration
        if calibration is None:
            calibration = CalibrationSettings(
                sad_boost=config.DEFAULT_SAD_BOOST,
                anger_boost=config.DEFAULT_ANGER_BOOST,
                neutral_suppress=config.DEFAULT_NEUTRAL_SUPPRESS
            )

        session = SessionData(
            session_id=session_id,
            start_time=datetime.now(),
            calibration=calibration
        )

        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionData]:
        """
        Get a session by ID.

        Args:
            session_id (str): Session UUID

        Returns:
            Optional[SessionData]: Session object or None if not found
        """
        return self._sessions.get(session_id)

    def end_session(self, session_id: str) -> Optional[SessionData]:
        """
        End an active session.

        Args:
            session_id (str): Session UUID

        Returns:
            Optional[SessionData]: Ended session object or None if not found
        """
        session = self._sessions.get(session_id)
        if session:
            session.is_active = False
            session.end_time = datetime.now()
        return session

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session permanently.

        Args:
            session_id (str): Session UUID

        Returns:
            bool: True if session was deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def update_calibration(
        self,
        session_id: str,
        calibration: CalibrationSettings
    ) -> bool:
        """
        Update calibration settings for a session.

        Args:
            session_id (str): Session UUID
            calibration (CalibrationSettings): New calibration settings

        Returns:
            bool: True if updated, False if session not found
        """
        session = self._sessions.get(session_id)
        if session:
            session.calibration = calibration
            return True
        return False

    def add_emotion_data(
        self,
        session_id: str,
        emotion_probs: Dict[str, float]
    ) -> bool:
        """
        Add emotion probability data to a session.

        Args:
            session_id (str): Session UUID
            emotion_probs (Dict[str, float]): Emotion probabilities

        Returns:
            bool: True if added, False if session not found
        """
        session = self._sessions.get(session_id)
        if session and session.is_active:
            session.add_emotion_data(emotion_probs)
            return True
        return False

    def get_active_sessions(self) -> List[SessionData]:
        """Get all active sessions."""
        return [s for s in self._sessions.values() if s.is_active]

    def get_session_count(self) -> int:
        """Get total number of sessions (active + inactive)."""
        return len(self._sessions)

    def _cleanup_expired_sessions(self):
        """Remove expired inactive sessions to free memory."""
        now = datetime.now()
        timeout = timedelta(minutes=self._timeout_minutes)

        expired_ids = []
        for session_id, session in self._sessions.items():
            if not session.is_active:
                time_since_end = now - (session.end_time or session.start_time)
                if time_since_end > timeout:
                    expired_ids.append(session_id)

        for session_id in expired_ids:
            del self._sessions[session_id]

        if expired_ids:
            print(f"Cleaned up {len(expired_ids)} expired sessions")


# Global session manager instance
session_manager = SessionManager()
