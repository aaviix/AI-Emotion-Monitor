// Main Dashboard Page

'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { VideoStream } from '@/src/components/video/VideoStream';
import { EmotionBarChart } from '@/src/components/charts/EmotionBarChart';
import { TimeSeriesChart } from '@/src/components/charts/TimeSeriesChart';
import { CalibrationPanel } from '@/src/components/controls/CalibrationPanel';
import { useEmotionStore } from '@/src/lib/store';
import { AlertCircle, BarChart3, Brain } from 'lucide-react';

export default function DashboardPage() {
  const { currentSession, isStreaming, streamError } = useEmotionStore();
  const [videoError, setVideoError] = useState<Error | null>(null);

  const sessionId = currentSession?.session_id || null;
  const isSessionActive = currentSession?.is_active || false;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="text-primary-600" size={32} />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AI Emotion Monitor</h1>
                <p className="text-sm text-gray-500">Clinical Dashboard</p>
              </div>
            </div>

            {currentSession && !isSessionActive && (
              <Link
                href={`/analytics/${currentSession.session_id}`}
                className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                <BarChart3 size={20} />
                View Analytics Report
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Alerts */}
        {(streamError || videoError) && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="text-red-600 flex-shrink-0" size={20} />
            <div>
              <p className="text-red-800 font-medium">Error</p>
              <p className="text-red-700 text-sm">{streamError || videoError?.message}</p>
            </div>
          </div>
        )}

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Video and Timeline */}
          <div className="lg:col-span-2 space-y-6">
            {/* Video Stream */}
            <VideoStream
              sessionId={sessionId}
              enabled={isSessionActive}
              onError={setVideoError}
            />

            {/* Timeline */}
            <TimeSeriesChart />
          </div>

          {/* Right Column - Controls and Current Emotions */}
          <div className="space-y-6">
            {/* Calibration Panel */}
            <CalibrationPanel />

            {/* Current Emotions */}
            <EmotionBarChart />
          </div>
        </div>

        {/* Instructions (shown when no session) */}
        {!currentSession && (
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-blue-900 font-semibold mb-3">Getting Started</h3>
            <ol className="list-decimal list-inside space-y-2 text-blue-800">
              <li>Adjust calibration settings in the panel to the right (optional)</li>
              <li>Click "Start Session" to begin emotion monitoring</li>
              <li>Allow webcam access when prompted</li>
              <li>Position your face in the camera frame</li>
              <li>Emotion detection will begin automatically</li>
              <li>Click "Stop Session & Generate Report" when finished</li>
            </ol>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between text-sm text-gray-500">
            <p>AI Emotion Monitor v1.0</p>
            <div className="flex items-center gap-4">
              <span>Backend API: {process.env.NEXT_PUBLIC_API_URL}</span>
              <span className={`flex items-center gap-1.5 ${isStreaming ? 'text-green-600' : 'text-gray-400'}`}>
                <div className={`w-2 h-2 rounded-full ${isStreaming ? 'bg-green-600' : 'bg-gray-400'}`} />
                {isStreaming ? 'Streaming' : 'Idle'}
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
