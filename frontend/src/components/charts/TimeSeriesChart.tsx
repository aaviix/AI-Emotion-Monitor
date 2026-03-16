// TimeSeriesChart - Line chart showing emotion trends over time

'use client';

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useEmotionStore } from '@/src/lib/store';
import { EMOTION_COLORS, EMOTION_LABELS, EmotionLabel } from '@/src/lib/types';

interface TimeSeriesChartProps {
  emotionsToShow?: EmotionLabel[];
  maxDataPoints?: number;
}

export function TimeSeriesChart({
  emotionsToShow = ['Angry', 'Sad', 'Happy', 'Neutral', 'Surprise'],
  maxDataPoints = 100,
}: TimeSeriesChartProps) {
  const { emotionHistory, timestamps } = useEmotionStore();

  // Prepare data for chart
  const data = timestamps
    .slice(-maxDataPoints) // Show last N data points
    .map((timestamp, index) => {
      const emotions = emotionHistory[emotionHistory.length - maxDataPoints + index];
      return {
        time: timestamp.toFixed(1),
        ...emotions,
      };
    });

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Emotion Timeline</h3>

      {emotionHistory.length === 0 ? (
        <div className="flex items-center justify-center h-64 text-gray-400">
          <p>Start streaming to see emotion timeline</p>
        </div>
      ) : (
        <>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis
                dataKey="time"
                label={{ value: 'Time (seconds)', position: 'insideBottom', offset: -10, fill: '#6b7280' }}
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
              <Legend
                wrapperStyle={{ paddingTop: '20px' }}
                iconType="line"
              />
              {emotionsToShow.map((emotion) => (
                <Line
                  key={emotion}
                  type="monotone"
                  dataKey={emotion}
                  stroke={EMOTION_COLORS[emotion]}
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 4 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>

          <div className="mt-4 text-sm text-gray-500 text-center">
            Showing {data.length} data points (last {maxDataPoints} max)
          </div>
        </>
      )}
    </div>
  );
}
