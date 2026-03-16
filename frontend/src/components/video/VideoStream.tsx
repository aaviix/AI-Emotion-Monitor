// VideoStream component - Displays webcam feed with emotion overlays

'use client';

import React from 'react';
import { useEmotionStream } from '@/src/hooks/useEmotionStream';
import { useEmotionStore } from '@/src/lib/store';
import { DISTRESS_EMOTIONS } from '@/src/lib/types';
import { AlertCircle, Camera, CameraOff } from 'lucide-react';

interface VideoStreamProps {
  sessionId: string | null;
  enabled: boolean;
  onError?: (error: Error) => void;
}

export function VideoStream({ sessionId, enabled, onError }: VideoStreamProps) {
  const { videoRef, canvasRef, isInitialized, webcamError } = useEmotionStream({
    sessionId,
    enabled,
    frameRate: 6,
    onError,
  });

  const { currentEmotion, isStreaming } = useEmotionStore();

  // Determine emotion display color
  const emotionColor = currentEmotion && DISTRESS_EMOTIONS.includes(currentEmotion.dominant_emotion as any)
    ? 'text-red-500 bg-red-50 border-red-500'
    : 'text-green-500 bg-green-50 border-green-500';

  return (
    <div className="relative w-full">
      {/* Canvas (hidden, used for frame capture) */}
      <canvas ref={canvasRef} className="hidden" />

      {/* Video feed */}
      <div className="relative bg-gray-900 rounded-lg overflow-hidden shadow-lg aspect-video">
        {webcamError ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-red-400 p-8 text-center">
            <CameraOff size={48} className="mb-4" />
            <p className="text-lg font-medium mb-2">Webcam Error</p>
            <p className="text-sm text-gray-400">{webcamError}</p>
          </div>
        ) : !isInitialized ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400">
            <Camera size={48} className="mb-4 animate-pulse" />
            <p>Initializing webcam...</p>
          </div>
        ) : (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover"
          />
        )}

        {/* Streaming indicator */}
        {isStreaming && isInitialized && (
          <div className="absolute top-4 left-4 flex items-center gap-2 bg-red-600 text-white px-3 py-1.5 rounded-full text-sm font-medium shadow-lg">
            <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
            LIVE
          </div>
        )}

        {/* Emotion overlay */}
        {currentEmotion && isStreaming && (
          <div className="absolute bottom-4 left-4 right-4">
            <div className={`${emotionColor} border-2 rounded-lg px-4 py-3 backdrop-blur-sm bg-opacity-90`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-medium opacity-75 mb-1">DETECTED EMOTION</p>
                  <p className="text-2xl font-bold">{currentEmotion.dominant_emotion}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs font-medium opacity-75 mb-1">CONFIDENCE</p>
                  <p className="text-2xl font-bold">{(currentEmotion.confidence * 100).toFixed(1)}%</p>
                </div>
              </div>

              {currentEmotion.num_faces > 1 && (
                <div className="mt-2 pt-2 border-t border-current border-opacity-20">
                  <p className="text-xs opacity-75">
                    {currentEmotion.num_faces} faces detected
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* No faces detected warning */}
        {currentEmotion && currentEmotion.num_faces === 0 && isStreaming && (
          <div className="absolute inset-x-4 bottom-4">
            <div className="bg-yellow-500 bg-opacity-90 text-yellow-900 rounded-lg px-4 py-3 flex items-center gap-2">
              <AlertCircle size={20} />
              <p className="text-sm font-medium">No face detected. Please position yourself in frame.</p>
            </div>
          </div>
        )}
      </div>

      {/* Video info */}
      <div className="mt-2 text-xs text-gray-500 flex items-center justify-between">
        <span>
          {isInitialized ? '✓ Webcam active' : 'Initializing...'}
        </span>
        {currentEmotion?.timestamp && (
          <span>Session time: {currentEmotion.timestamp.toFixed(1)}s</span>
        )}
      </div>
    </div>
  );
}
