// Custom hook for session management

import { useState, useCallback } from 'react';
import { api } from '@/src/lib/api';
import { useEmotionStore } from '@/src/lib/store';
import { CalibrationSettings, SessionData } from '@/src/lib/types';

export function useSession() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    currentSession,
    setSession,
    calibration,
    updateCalibration: updateStoreCalibration,
    clearHistory,
    resetStore,
  } = useEmotionStore();

  const startSession = useCallback(
    async (customCalibration?: CalibrationSettings): Promise<SessionData | null> => {
      setLoading(true);
      setError(null);

      try {
        const sessionCalibration = customCalibration || calibration;
        const session = await api.startSession(sessionCalibration);

        setSession(session);
        clearHistory();

        return session;
      } catch (err: any) {
        const errorMsg = err?.response?.data?.error || err.message || 'Failed to start session';
        setError(errorMsg);
        console.error('Start session error:', err);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [calibration, setSession, clearHistory]
  );

  const stopSession = useCallback(async (): Promise<SessionData | null> => {
    if (!currentSession) {
      setError('No active session');
      return null;
    }

    setLoading(true);
    setError(null);

    try {
      const updatedSession = await api.stopSession(currentSession.session_id);
      setSession(updatedSession);

      return updatedSession;
    } catch (err: any) {
      const errorMsg = err?.response?.data?.error || err.message || 'Failed to stop session';
      setError(errorMsg);
      console.error('Stop session error:', err);
      return null;
    } finally {
      setLoading(false);
    }
  }, [currentSession, setSession]);

  const updateCalibration = useCallback(
    async (newCalibration: Partial<CalibrationSettings>): Promise<boolean> => {
      if (!currentSession) {
        setError('No active session');
        return false;
      }

      setLoading(true);
      setError(null);

      try {
        const fullCalibration = { ...calibration, ...newCalibration };
        await api.updateCalibration(currentSession.session_id, fullCalibration);

        // Update local store
        updateStoreCalibration(newCalibration);

        return true;
      } catch (err: any) {
        const errorMsg =
          err?.response?.data?.error || err.message || 'Failed to update calibration';
        setError(errorMsg);
        console.error('Update calibration error:', err);
        return false;
      } finally {
        setLoading(false);
      }
    },
    [currentSession, calibration, updateStoreCalibration]
  );

  const resetSession = useCallback(() => {
    resetStore();
    setError(null);
  }, [resetStore]);

  return {
    currentSession,
    isActive: currentSession?.is_active || false,
    loading,
    error,
    startSession,
    stopSession,
    updateCalibration,
    resetSession,
    calibration,
  };
}
