// Analytics page - Clinical assessment report for completed sessions

'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { api } from '@/src/lib/api';
import { AnalyticsSummary, TimeseriesData, EMOTION_COLORS, EMOTION_LABELS } from '@/src/lib/types';
import { ArrowLeft, Brain, AlertCircle, CheckCircle, Info, TrendingUp, Clock, Activity } from 'lucide-react';

export default function AnalyticsPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.sessionId as string;

  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [timeseries, setTimeseries] = useState<TimeseriesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hasNoData, setHasNoData] = useState(false);

  useEffect(() => {
    const fetchAnalytics = async () => {
      if (!sessionId) return;

      setLoading(true);
      setError(null);
      setHasNoData(false);

      try {
        const [analyticsData, timeseriesData] = await Promise.all([
          api.getAnalyticsSummary(sessionId),
          api.getTimeseries(sessionId, 50),
        ]);

        setAnalytics(analyticsData);
        setTimeseries(timeseriesData);
      } catch (err: any) {
        const errorMsg = err?.response?.data?.error || err.message || 'Failed to load analytics';
        if (errorMsg === 'No emotion data available for this session') {
          setHasNoData(true);
        }
        setError(errorMsg);
        console.error('Analytics fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, [sessionId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (hasNoData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
          <Info className="text-blue-600 mx-auto mb-4" size={48} />
          <h2 className="text-xl font-bold text-gray-900 mb-2">No Emotion Data Captured</h2>
          <p className="text-gray-600 mb-2">
            This session ended before any frames were analyzed.
          </p>
          <p className="text-gray-600 mb-4">
            Start a new session and keep the webcam active for a few seconds before stopping.
          </p>
          <Link
            href="/"
            className="block w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg text-center transition-colors"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  if (error || !analytics) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
          <AlertCircle className="text-red-600 mx-auto mb-4" size={48} />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Error Loading Analytics</h2>
          <p className="text-gray-600 mb-4">{error || 'Session not found'}</p>
          <Link
            href="/"
            className="block w-full bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg text-center transition-colors"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  // Prepare data for charts
  const avgEmotionData = EMOTION_LABELS.map((emotion) => ({
    emotion,
    probability: analytics.avg_emotions[emotion],
    percentage: (analytics.avg_emotions[emotion] * 100).toFixed(1),
  }));

  const timeseriesData = timeseries?.timestamps.map((time, idx) => ({
    time: time.toFixed(1),
    ...timeseries.emotions[idx],
  })) || [];

  // Assessment level styling
  const assessmentStyles = {
    warning: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-800',
      icon: AlertCircle,
    },
    success: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      text: 'text-green-800',
      icon: CheckCircle,
    },
    info: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      text: 'text-blue-800',
      icon: Info,
    },
  };

  const levelStyle = assessmentStyles[analytics.assessment.level];
  const LevelIcon = levelStyle.icon;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="text-primary-600" size={32} />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Therapeutic Analytics Report</h1>
                <p className="text-sm text-gray-500">Session: {sessionId.slice(0, 8)}...</p>
              </div>
            </div>

            <Link
              href="/"
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              <ArrowLeft size={20} />
              Back to Dashboard
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Session Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-3 mb-2">
              <Clock className="text-primary-600" size={24} />
              <span className="text-sm text-gray-600">Duration</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {(analytics.duration_seconds / 60).toFixed(1)} min
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-3 mb-2">
              <Activity className="text-primary-600" size={24} />
              <span className="text-sm text-gray-600">Frames Analyzed</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{analytics.num_frames}</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-3 mb-2">
              <TrendingUp className="text-red-600" size={24} />
              <span className="text-sm text-gray-600">Distress Score</span>
            </div>
            <p className="text-2xl font-bold text-red-600">
              {(analytics.distress_score * 100).toFixed(1)}%
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-3 mb-2">
              <CheckCircle className="text-green-600" size={24} />
              <span className="text-sm text-gray-600">Stability Score</span>
            </div>
            <p className="text-2xl font-bold text-green-600">
              {(analytics.stability_score * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        {/* Clinical Assessment */}
        <div className={`${levelStyle.bg} border ${levelStyle.border} rounded-lg p-6 mb-8`}>
          <div className="flex items-start gap-4">
            <LevelIcon className={levelStyle.text} size={32} />
            <div className="flex-1">
              <h2 className={`text-xl font-bold ${levelStyle.text} mb-2`}>
                Clinical Assessment
              </h2>
              <p className={`text-lg font-semibold ${levelStyle.text} mb-4`}>
                {analytics.assessment.summary}
              </p>

              {/* Details */}
              {analytics.assessment.details.map((detail, idx) => (
                <div key={idx} className={`mt-4 p-4 bg-white rounded-lg border ${levelStyle.border}`}>
                  <p className={`font-medium ${levelStyle.text} mb-1`}>{detail.message}</p>
                  {detail.description && (
                    <p className="text-gray-700 text-sm">{detail.description}</p>
                  )}
                </div>
              ))}

              {/* Recommendations */}
              {analytics.assessment.recommendations.length > 0 && (
                <div className="mt-6">
                  <h3 className={`font-semibold ${levelStyle.text} mb-3`}>Recommendations:</h3>
                  <ul className="space-y-2">
                    {analytics.assessment.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className={levelStyle.text}>•</span>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Average Emotions */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Average Emotional Profile</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={avgEmotionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="emotion" angle={-45} textAnchor="end" height={80} />
                <YAxis domain={[0, 1]} />
                <Tooltip formatter={(value: number) => `${(value * 100).toFixed(1)}%`} />
                <Bar dataKey="probability" radius={[8, 8, 0, 0]}>
                  {avgEmotionData.map((entry) => (
                    <Cell key={entry.emotion} fill={EMOTION_COLORS[entry.emotion]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Timeseries */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">Longitudinal Session Arc</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={timeseriesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" label={{ value: 'Time (s)', position: 'insideBottom', offset: -10 }} />
                <YAxis domain={[0, 1]} />
                <Tooltip />
                <Legend />
                {['Angry', 'Sad', 'Happy', 'Neutral', 'Surprise'].map((emotion) => (
                  <Line
                    key={emotion}
                    type="monotone"
                    dataKey={emotion}
                    stroke={EMOTION_COLORS[emotion as keyof typeof EMOTION_COLORS]}
                    strokeWidth={2}
                    dot={false}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
}
