// EmotionBarChart - Bar chart showing current emotion probabilities

'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { useEmotionStore } from '@/src/lib/store';
import { EMOTION_COLORS, EMOTION_LABELS } from '@/src/lib/types';

export function EmotionBarChart() {
  const { currentEmotion } = useEmotionStore();

  // Prepare data for chart
  const data = EMOTION_LABELS.map((emotion) => ({
    emotion,
    probability: currentEmotion?.emotion_probs[emotion] || 0,
    percentage: ((currentEmotion?.emotion_probs[emotion] || 0) * 100).toFixed(1),
  }));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Current Emotion Probabilities</h3>

      {!currentEmotion ? (
        <div className="flex items-center justify-center h-64 text-gray-400">
          <p>Start streaming to see emotion data</p>
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="emotion"
              angle={-45}
              textAnchor="end"
              height={80}
              tick={{ fill: '#6b7280', fontSize: 12 }}
            />
            <YAxis
              domain={[0, 1]}
              ticks={[0, 0.25, 0.5, 0.75, 1]}
              tick={{ fill: '#6b7280', fontSize: 12 }}
              label={{ value: 'Probability', angle: -90, position: 'insideLeft', fill: '#6b7280' }}
            />
            <Tooltip
              formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '0.5rem',
                padding: '0.5rem',
              }}
            />
            <Bar dataKey="probability" radius={[8, 8, 0, 0]}>
              {data.map((entry) => (
                <Cell key={entry.emotion} fill={EMOTION_COLORS[entry.emotion]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}

      {/* Dominant emotion display */}
      {currentEmotion && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Dominant Emotion:</span>
            <span
              className="text-lg font-bold"
              style={{ color: EMOTION_COLORS[currentEmotion.dominant_emotion] }}
            >
              {currentEmotion.dominant_emotion} ({(currentEmotion.confidence * 100).toFixed(1)}%)
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
