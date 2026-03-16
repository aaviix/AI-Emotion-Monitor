"""
Clinical analytics engine for therapeutic assessment generation.

This module provides functions for analyzing emotion data from clinical sessions:
- Average emotion probabilities
- Distress and stability scores
- Clinical assessment generation
- Cognitive shift detection

Implements the same analytics logic as the original Streamlit dashboard.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def calculate_avg_emotions(emotion_history: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Calculate average emotion probabilities across a session.

    Args:
        emotion_history (List[Dict[str, float]]): List of emotion probability dictionaries

    Returns:
        Dict[str, float]: Average probability for each emotion
    """
    if not emotion_history:
        return {}

    df = pd.DataFrame(emotion_history)
    return df.mean().to_dict()


def calculate_distress_score(avg_emotions: Dict[str, float]) -> float:
    """
    Calculate distress score (sum of negative affect emotions).

    Args:
        avg_emotions (Dict[str, float]): Average emotion probabilities

    Returns:
        float: Distress score (sum of Angry, Disgust, Fear, Sad)
    """
    distress_emotions = ['Angry', 'Disgust', 'Fear', 'Sad']
    return sum(avg_emotions.get(emotion, 0.0) for emotion in distress_emotions)


def calculate_stability_score(avg_emotions: Dict[str, float]) -> float:
    """
    Calculate stability score (sum of positive/neutral emotions).

    Args:
        avg_emotions (Dict[str, float]): Average emotion probabilities

    Returns:
        float: Stability score (sum of Happy, Neutral)
    """
    stability_emotions = ['Happy', 'Neutral']
    return sum(avg_emotions.get(emotion, 0.0) for emotion in stability_emotions)


def detect_cognitive_shift(avg_emotions: Dict[str, float], threshold: float = 0.20) -> bool:
    """
    Detect significant cognitive shift (high Surprise level).

    High surprise levels may indicate therapeutic breakthroughs or
    moments of realization during a clinical session.

    Args:
        avg_emotions (Dict[str, float]): Average emotion probabilities
        threshold (float): Surprise probability threshold (default: 0.20)

    Returns:
        bool: True if cognitive shift detected
    """
    surprise_level = avg_emotions.get('Surprise', 0.0)
    return surprise_level > threshold


def generate_clinical_assessment(
    avg_emotions: Dict[str, float],
    distress_score: float,
    stability_score: float
) -> Dict[str, any]:
    """
    Generate a comprehensive clinical assessment report.

    Args:
        avg_emotions (Dict[str, float]): Average emotion probabilities
        distress_score (float): Calculated distress score
        stability_score (float): Calculated stability score

    Returns:
        Dict[str, any]: Clinical assessment with insights and recommendations
    """
    assessment = {
        'summary': '',
        'level': 'info',  # 'info', 'warning', or 'success'
        'details': [],
        'recommendations': []
    }

    # Detect cognitive shift
    has_cognitive_shift = detect_cognitive_shift(avg_emotions)
    if has_cognitive_shift:
        assessment['details'].append({
            'type': 'cognitive_shift',
            'message': f"Significant 'Cognitive Shift' detected (Surprise: {avg_emotions.get('Surprise', 0):.1%})",
            'description': "Patient may have experienced moments of realization or emotional breakthrough during the session."
        })

    # Overall emotional state assessment
    if distress_score > stability_score:
        assessment['level'] = 'warning'
        assessment['summary'] = f"High Negative Affect Detected ({distress_score:.1%})"
        assessment['details'].append({
            'type': 'high_distress',
            'message': "The patient exhibited frequent indicators of emotional imbalance.",
            'description': "Sustained distress detected throughout the session."
        })

        # Specific emotion recommendations
        if avg_emotions.get('Sad', 0) > 0.15:
            assessment['recommendations'].append(
                "Consider screening for depressive symptoms given elevated sadness levels."
            )
        if avg_emotions.get('Angry', 0) > 0.15:
            assessment['recommendations'].append(
                "Elevated anger levels detected. Explore potential stressors or frustrations."
            )
        if avg_emotions.get('Fear', 0) > 0.15:
            assessment['recommendations'].append(
                "Significant fear/anxiety observed. Consider anxiety assessment protocols."
            )

    else:
        assessment['level'] = 'success'
        assessment['summary'] = f"High Emotional Stability Detected ({stability_score:.1%})"
        assessment['details'].append({
            'type': 'stability',
            'message': "The patient demonstrated consistent emotional regulation throughout the session.",
            'description': "Positive indicators of emotional balance and stability."
        })

        assessment['recommendations'].append(
            "Continue current therapeutic approach. Patient shows good emotional regulation."
        )

    # Dominant emotion analysis
    dominant_emotion = max(avg_emotions.items(), key=lambda x: x[1])
    assessment['details'].append({
        'type': 'dominant_emotion',
        'emotion': dominant_emotion[0],
        'probability': dominant_emotion[1],
        'message': f"Dominant emotion: {dominant_emotion[0]} ({dominant_emotion[1]:.1%})"
    })

    return assessment


def generate_timeseries_summary(
    emotion_history: List[Dict[str, float]],
    timestamps: List[float],
    window_size: int = 30
) -> Dict[str, List[Dict[str, float]]]:
    """
    Generate time-series summary with windowed averages.

    Useful for plotting emotion trends over time.

    Args:
        emotion_history (List[Dict[str, float]]): Emotion probability history
        timestamps (List[float]): Corresponding timestamps (seconds)
        window_size (int): Number of frames to average (default: 30)

    Returns:
        Dict[str, List[Dict[str, float]]]: Time-series data for each emotion
    """
    if not emotion_history or len(emotion_history) < window_size:
        # Return raw data if insufficient for windowing
        return {
            'timestamps': timestamps,
            'emotions': emotion_history
        }

    df = pd.DataFrame(emotion_history)
    df['timestamp'] = timestamps

    # Apply rolling average for smoothing
    smoothed = df.rolling(window=window_size, min_periods=1).mean()

    result = {
        'timestamps': smoothed['timestamp'].tolist(),
        'emotions': smoothed.drop('timestamp', axis=1).to_dict('records')
    }

    return result


def get_emotion_distribution(emotion_history: List[Dict[str, float]]) -> Dict[str, int]:
    """
    Get the distribution of dominant emotions across the session.

    Counts how many frames each emotion was dominant.

    Args:
        emotion_history (List[Dict[str, float]]): Emotion probability history

    Returns:
        Dict[str, int]: Count of frames where each emotion was dominant
    """
    distribution = {}

    for probs in emotion_history:
        dominant = max(probs.items(), key=lambda x: x[1])[0]
        distribution[dominant] = distribution.get(dominant, 0) + 1

    return distribution


def calculate_emotion_variability(emotion_history: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Calculate variability (standard deviation) for each emotion across the session.

    High variability may indicate emotional instability or reactivity.

    Args:
        emotion_history (List[Dict[str, float]]): Emotion probability history

    Returns:
        Dict[str, float]: Standard deviation for each emotion
    """
    if not emotion_history:
        return {}

    df = pd.DataFrame(emotion_history)
    return df.std().to_dict()
