// CalibrationPanel - Controls for session and emotion sensitivity

'use client';

import React, { useState, useEffect } from 'react';
import { useSession } from '@/src/hooks/useSession';
import { useEmotionStore } from '@/src/lib/store';
import { Play, Square, RotateCcw, Settings, Info } from 'lucide-react';

export function CalibrationPanel() {
  const { startSession, stopSession, updateCalibration, isActive, loading, currentSession } = useSession();
  const { calibration, updateCalibration: updateStoreCalibration, emotionHistory, resetStore } = useEmotionStore();

  const [localCalibration, setLocalCalibration] = useState(calibration);

  // Sync local state with store
  useEffect(() => {
    setLocalCalibration(calibration);
  }, [calibration]);

  const handleStart = async () => {
    await startSession(localCalibration);
  };

  const handleStop = async () => {
    await stopSession();
  };

  const handleReset = () => {
    if (confirm('Reset all data? This will clear emotion history and end the current session.')) {
      resetStore();
    }
  };

  const handleCalibrationChange = (key: keyof typeof calibration, value: number) => {
    const newCalibration = { ...localCalibration, [key]: value };
    setLocalCalibration(newCalibration);
    updateStoreCalibration({ [key]: value });

    // If session is active, update via API
    if (isActive) {
      updateCalibration({ [key]: value });
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center gap-2 mb-6">
        <Settings className="text-primary-600" size={24} />
        <h3 className="text-lg font-semibold text-gray-900">Calibration Panel</h3>
      </div>

      <div className="mb-6 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800 flex items-start gap-2">
        <Info size={16} className="flex-shrink-0 mt-0.5" />
        <p>
          Adjust sensitivity to compensate for lighting or individual patient baselines.
        </p>
      </div>

      {/* Calibration Sliders */}
      <div className="space-y-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sadness Sensitivity
            <span className="ml-2 text-primary-600 font-semibold">{localCalibration.sad_boost.toFixed(1)}</span>
          </label>
          <input
            type="range"
            min="1.0"
            max="5.0"
            step="0.1"
            value={localCalibration.sad_boost}
            onChange={(e) => handleCalibrationChange('sad_boost', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Low (1.0)</span>
            <span>High (5.0)</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Anger Sensitivity
            <span className="ml-2 text-primary-600 font-semibold">{localCalibration.anger_boost.toFixed(1)}</span>
          </label>
          <input
            type="range"
            min="1.0"
            max="5.0"
            step="0.1"
            value={localCalibration.anger_boost}
            onChange={(e) => handleCalibrationChange('anger_boost', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Low (1.0)</span>
            <span>High (5.0)</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Neutrality Suppression
            <span className="ml-2 text-primary-600 font-semibold">{localCalibration.neutral_suppress.toFixed(2)}</span>
          </label>
          <input
            type="range"
            min="0.0"
            max="1.0"
            step="0.05"
            value={localCalibration.neutral_suppress}
            onChange={(e) => handleCalibrationChange('neutral_suppress', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>None (0.0)</span>
            <span>Max (1.0)</span>
          </div>
        </div>
      </div>

      {/* Session Controls */}
      <div className="space-y-3 pt-6 border-t border-gray-200">
        {!isActive ? (
          <button
            onClick={handleStart}
            disabled={loading}
            className="w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play size={20} />
            {loading ? 'Starting...' : 'Start Session'}
          </button>
        ) : (
          <button
            onClick={handleStop}
            disabled={loading}
            className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Square size={20} />
            {loading ? 'Stopping...' : 'Stop Session & Generate Report'}
          </button>
        )}

        <button
          onClick={handleReset}
          disabled={loading}
          className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RotateCcw size={20} />
          Reset All Data
        </button>
      </div>

      {/* Session Info */}
      {currentSession && (
        <div className="mt-6 pt-6 border-t border-gray-200 space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Session ID:</span>
            <span className="font-mono text-xs text-gray-900">
              {currentSession.session_id.slice(0, 8)}...
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Duration:</span>
            <span className="font-medium text-gray-900">
              {currentSession.duration_seconds.toFixed(1)}s
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Frames Captured:</span>
            <span className="font-medium text-gray-900">{emotionHistory.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Status:</span>
            <span className={`font-medium ${isActive ? 'text-green-600' : 'text-gray-600'}`}>
              {isActive ? '● Active' : '○ Inactive'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
