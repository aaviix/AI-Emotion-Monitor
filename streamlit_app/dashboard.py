"""
Enhanced Streamlit Clinical Dashboard for AI Emotion Monitor.

This refactored version uses shared backend modules for code reusability
while maintaining all original functionality from clinical_dashboard.py.

Features:
- Real-time emotion detection with webcam
- CLAHE preprocessing for clinical lighting conditions
- Temporal smoothing with probability buffer
- Clinical calibration panel
- Session analytics and therapeutic assessment

Run: streamlit run streamlit_app/dashboard.py
"""

import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time
import sys
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.inference import EmotionInferenceEngine, CalibrationSettings
from backend.services.analytics_engine import (
    calculate_avg_emotions,
    calculate_distress_score,
    calculate_stability_score,
    generate_clinical_assessment
)
from backend.utils.config import config


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================
st.set_page_config(page_title="AI Mental Health Monitor", layout="wide")


# ============================================================
# LOAD EMOTION INFERENCE ENGINE (CACHED)
# ============================================================
@st.cache_resource
def load_inference_engine():
    """Load the emotion inference engine (cached for performance)."""
    try:
        engine = EmotionInferenceEngine(
            model_path=config.MODEL_PATH,
            device=config.DEVICE,
            enable_smoothing=True,
            smoothing_window=8,
            enable_calibration=True
        )
        return engine
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.stop()


# Initialize inference engine
inference_engine = load_inference_engine()
EMOTIONS = inference_engine.get_emotion_labels()


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "timestamps" not in st.session_state:
    st.session_state.timestamps = []


# ============================================================
# UI LAYOUT
# ============================================================
st.title("🧠 Mental Health Real-Time Analytics (FER2013)")
st.markdown("### Clinical Monitoring Dashboard")

with st.sidebar:
    st.header("⚙️ Calibration Panel")
    st.info("Adjust sensitivity to compensate for lighting or individual baseline differences.")

    # Calibration sliders
    sad_boost = st.slider("Sadness Sensitivity", 1.0, 5.0, 2.5, 0.1)
    anger_boost = st.slider("Anger Sensitivity", 1.0, 5.0, 2.0, 0.1)
    neutral_suppress = st.slider("Neutrality Suppression", 0.0, 1.0, 0.3, 0.05)

    # Update calibration settings
    calibration = CalibrationSettings(
        sad_boost=sad_boost,
        anger_boost=anger_boost,
        neutral_suppress=neutral_suppress
    )
    inference_engine.update_calibration(calibration)

    st.divider()

    # Session controls
    start_btn = st.button("▶️ Start 10-Min Session", use_container_width=True)
    stop_btn = st.button("⏹️ End & Generate Report", use_container_width=True)

    if st.button("🗑️ Reset All Data", use_container_width=True):
        st.session_state.history = []
        st.session_state.timestamps = []
        inference_engine.reset_smoothing_buffer()
        st.rerun()

# Main content area
col_video, col_metrics = st.columns([2, 1])
webcam_placeholder = col_video.empty()
chart_placeholder = col_metrics.empty()


# ============================================================
# VIDEO PROCESSING LOOP
# ============================================================
if start_btn:
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    inference_engine.reset_smoothing_buffer()  # Reset for new session

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or stop_btn:
            break

        current_elapsed = time.time() - start_time

        # Run emotion detection
        result = inference_engine.detect_emotion(frame, apply_clahe=True)

        # Store in session history
        st.session_state.history.append(result.emotion_probs)
        st.session_state.timestamps.append(current_elapsed)

        # Draw face detection and emotion label on frame
        for face in result.faces:
            x, y, w, h = face

            # Color based on emotion type
            is_distress = result.dominant_emotion in ['Angry', 'Sad', 'Fear', 'Disgust']
            color = (0, 0, 255) if is_distress else (0, 255, 0)

            # Draw rectangle and label
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            label_text = f"{result.dominant_emotion}: {result.confidence:.1%}"
            cv2.putText(frame, label_text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Display video frame
        webcam_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

        # Display emotion probabilities chart
        prob_df = pd.DataFrame([result.emotion_probs], columns=EMOTIONS).T
        prob_df.columns = ['Intensity']
        chart_placeholder.bar_chart(prob_df)

    cap.release()
    st.success("✅ Session finished. Analysis report ready.")


# ============================================================
# CLINICAL ASSESSMENT REPORT
# ============================================================
if not start_btn and len(st.session_state.history) > 0:
    st.divider()
    st.header("📊 Therapeutic Analytics Report")

    # Calculate analytics
    avg_emotions = calculate_avg_emotions(st.session_state.history)
    distress_score = calculate_distress_score(avg_emotions)
    stability_score = calculate_stability_score(avg_emotions)
    assessment = generate_clinical_assessment(avg_emotions, distress_score, stability_score)

    # Display average emotions and time-series
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Average Emotional Profile")
        avg_df = pd.Series(avg_emotions)
        st.bar_chart(avg_df)

    with c2:
        st.subheader("Longitudinal Session Arc")
        # Create time-series dataframe
        history_df = pd.DataFrame(st.session_state.history, columns=EMOTIONS)
        history_df['Time'] = st.session_state.timestamps
        st.line_chart(history_df.set_index('Time')[['Sad', 'Angry', 'Happy', 'Neutral', 'Surprise']])

    # Display clinical assessment
    st.divider()
    st.subheader("🩺 Therapeutic Assessment")

    # Summary with appropriate level
    if assessment['level'] == 'warning':
        st.warning(f"**Assessment:** {assessment['summary']}")
    elif assessment['level'] == 'success':
        st.success(f"**Assessment:** {assessment['summary']}")
    else:
        st.info(f"**Assessment:** {assessment['summary']}")

    # Details
    for detail in assessment['details']:
        if detail['type'] == 'cognitive_shift':
            st.info(f"**Insight:** {detail['message']}")
            st.write(detail['description'])
        elif detail['type'] == 'high_distress':
            st.write(detail['message'])
            st.write(detail['description'])
        elif detail['type'] == 'stability':
            st.write(detail['message'])
            st.write(detail['description'])

    # Recommendations
    if assessment['recommendations']:
        st.subheader("📋 Recommendations")
        for rec in assessment['recommendations']:
            st.write(f"• {rec}")

    # Session statistics
    st.divider()
    st.subheader("📈 Session Statistics")

    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.metric("Duration", f"{st.session_state.timestamps[-1]:.1f}s")
    with stats_col2:
        st.metric("Total Frames", len(st.session_state.history))
    with stats_col3:
        dominant = max(avg_emotions.items(), key=lambda x: x[1])
        st.metric("Dominant Emotion", f"{dominant[0]} ({dominant[1]:.1%})")
