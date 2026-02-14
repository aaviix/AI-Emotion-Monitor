# AI-Driven Emotional Intelligence Monitor for Mental Health
AI-Driven Emotional Intelligence Monitor for Mental Health. Developed for the Deep Learning Module (MSc. AIM) at HFU. Features an Improved CNN (65.9% accuracy), CLAHE preprocessing, and a real-time Streamlit dashboard for longitudinal affective tracking.

## 📖 Overview
This project transitions qualitative clinical observations into objective, quantitative data. By utilizing a robust Deep Learning framework, we provide mental health professionals with a real-time monitor to track patient emotional states over time.

### Key Objectives
* **Detection:** Classify 7 complex human emotional states (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral) from facial imagery.
* **Temporal Tracking:** Implement longitudinal patterns to assist professionals in identifying mood fluctuations and early warning signs.
* **Clinical Utility:** Build a robust interface that handles real-world environmental challenges like poor clinical lighting.

---

## 🛠️ Technical Architecture

### 🧠 The Model: Improved CNN
Our model evolved from a baseline "Sanity Check" (100% accuracy on small batches) to a deep architecture featuring:
* **Double-Convolution Blocks:** For hierarchical feature extraction.
* **Global Average Pooling (GAP):** To reduce parameters and prevent overfitting.
* **Softmax Output:** Generating probabilities across the 7 FER2013 emotion categories.


### ⚙️ Clinical Preprocessing Pipeline
To ensure the model is "clinical-ready," we implemented:
1.  **Haar Cascades:** Real-time facial landmark isolation via OpenCV.
2.  **CLAHE (Contrast Limited Adaptive Histogram Equalization):** Critical for mitigating "yellow light" issues or poor clinical lighting that can obscure micro-expressions.
3.  **Temporal Smoothing:** A **deque probability buffer (maxlen=8)** to prevent "flickering" in emotion labels, providing a stable visual experience for the professional.

---

## 📊 Performance & Validation
* **Dataset:** FER2013 (Facial Expression Recognition 2013).
* **Empirical Performance:** Achieved **65.9% test accuracy**, significantly exceeding the 14.3% random-guess threshold.
* **Clinical Validation:** Evaluated using accuracy, F1-scores, and confusion matrices to move beyond simple classification toward reliable longitudinal monitoring.

---

## 🖥️ The Clinical Dashboard (Implementation)
The system is deployed via a **Streamlit Dashboard** which features:
* **Real-Time Affective Analytics:** Live video feed with stabilized emotion overlays.
* **Therapeutic Analytics Report:** Longitudinal graphs tracking emotional shifts and "Cognitive Shifts" throughout a session.
* **Calibration Panel:** Allows clinicians to adjust sensitivity for individual patient baselines and environmental factors.

---

## 🚀 The Road Ahead: Optimization
While 65.9% is a strong academic benchmark for the FER2013 dataset, the system **requires further optimization** to reach clinical-grade reliability. Future iterations will focus on:
* **Hyperparameter Tuning:** Refining dropout rates and learning schedules to minimize generalization error.
* **Data Augmentation:** Increasing dataset diversity to handle varied facial orientations and occlusions.
* **Transformer Architectures:** Exploring **Vision Transformers (ViTs)** for more nuanced global feature extraction.

---
