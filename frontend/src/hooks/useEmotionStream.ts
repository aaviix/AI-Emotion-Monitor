// Custom hook for emotion streaming from webcam

import { useEffect, useRef, useCallback, useState } from 'react';
import { api } from '@/src/lib/api';
import { useEmotionStore } from '@/src/lib/store';
import { EmotionResult } from '@/src/lib/types';

interface UseEmotionStreamOptions {
  sessionId: string | null;
  enabled: boolean;
  frameRate?: number; // Frames per second (default: 5-7 fps)
  onFrameProcessed?: (emotion: EmotionResult) => void;
  onError?: (error: Error) => void;
}

export function useEmotionStream({
  sessionId,
  enabled,
  frameRate = 6,
  onFrameProcessed,
  onError,
}: UseEmotionStreamOptions) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const [isInitialized, setIsInitialized] = useState(false);
  const [webcamError, setWebcamError] = useState<string | null>(null);

  const {
    setCurrentEmotion,
    addEmotionToHistory,
    setIsStreaming,
    setStreamError,
  } = useEmotionStore();

  // Initialize webcam
  const initializeWebcam = useCallback(async () => {
    try {
      setWebcamError(null);

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user',
        },
      });

      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      setIsInitialized(true);
    } catch (err: any) {
      const errorMsg = err.name === 'NotAllowedError'
        ? 'Webcam access denied. Please allow camera permissions.'
        : err.name === 'NotFoundError'
        ? 'No webcam found. Please connect a camera.'
        : `Webcam error: ${err.message}`;

      setWebcamError(errorMsg);
      onError?.(new Error(errorMsg));
      console.error('Webcam initialization error:', err);
    }
  }, [onError]);

  // Capture frame and send to API
  const captureAndProcessFrame = useCallback(async () => {
    if (!sessionId || !videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    // Ensure video is ready
    if (video.readyState !== video.HAVE_ENOUGH_DATA) return;

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to base64
    const imageBase64 = canvas.toDataURL('image/jpeg', 0.8);

    try {
      // Send to API
      const emotionResult = await api.streamEmotionFrame(sessionId, imageBase64);

      // Update store
      setCurrentEmotion(emotionResult);
      addEmotionToHistory(emotionResult.emotion_probs, emotionResult.timestamp || 0);

      // Callback
      onFrameProcessed?.(emotionResult);

      setStreamError(null);
    } catch (err: any) {
      const errorMsg = err?.response?.data?.error || err.message || 'Stream processing failed';
      setStreamError(errorMsg);
      onError?.(new Error(errorMsg));
      console.error('Frame processing error:', err);
    }
  }, [sessionId, setCurrentEmotion, addEmotionToHistory, setStreamError, onFrameProcessed, onError]);

  // Start streaming
  const startStreaming = useCallback(() => {
    if (!enabled || !sessionId || !isInitialized) return;

    setIsStreaming(true);

    // Capture frames at specified rate
    const intervalMs = 1000 / frameRate;
    intervalRef.current = setInterval(captureAndProcessFrame, intervalMs);
  }, [enabled, sessionId, isInitialized, frameRate, setIsStreaming, captureAndProcessFrame]);

  // Stop streaming
  const stopStreaming = useCallback(() => {
    setIsStreaming(false);

    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, [setIsStreaming]);

  // Cleanup webcam
  const cleanup = useCallback(() => {
    stopStreaming();

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setIsInitialized(false);
  }, [stopStreaming]);

  // Initialize webcam on mount
  useEffect(() => {
    initializeWebcam();

    return cleanup;
  }, [initializeWebcam, cleanup]);

  // Start/stop streaming based on enabled state
  useEffect(() => {
    if (enabled && sessionId && isInitialized) {
      startStreaming();
    } else {
      stopStreaming();
    }

    return stopStreaming;
  }, [enabled, sessionId, isInitialized, startStreaming, stopStreaming]);

  return {
    videoRef,
    canvasRef,
    isInitialized,
    webcamError,
    startStreaming,
    stopStreaming,
    cleanup,
  };
}
