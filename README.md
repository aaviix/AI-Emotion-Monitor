# AI-Driven Emotional Intelligence Monitor for Mental Health

Real-time emotion detection and monitoring system for mental health professionals. Developed for the Deep Learning Module (MSc. AIM) at HFU.

**Features:**
- 🧠 Improved CNN (65.9% accuracy on FER2013)
- 🎥 Real-time webcam emotion detection
- 📊 Longitudinal affective tracking
- 🏥 Clinical calibration controls
- 📈 Comprehensive analytics reports
- 🚀 Dual dashboard options (Next.js + Streamlit)

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

## 🖥️ Dual Dashboard Architecture

This project features **TWO fully-implemented dashboard options** to provide maximum flexibility:

### 1. **Flask API + Next.js Dashboard** (Production-Ready) ⭐

Modern, scalable architecture for professional deployment with enterprise-grade features.

**Backend: Flask REST API**
- Comprehensive REST endpoints for emotion detection, session management, and analytics
- Modular architecture with shared core modules (model, inference, preprocessing)
- Session state management with UUID-based tracking
- Clinical analytics engine with automated assessment generation
- CORS-enabled for cross-origin requests
- Configurable via environment variables

**Frontend: Next.js + TypeScript**
- **Real-time Video Streaming:** Webcam capture at 6 FPS with live emotion overlays
- **Interactive Visualizations:**
  - Real-time emotion probability bar chart (Recharts)
  - Time-series line chart tracking emotion trends
  - Color-coded emotion indicators (red=distress, green=positive)
- **Clinical Controls:**
  - Sadness Sensitivity slider (1.0-5.0)
  - Anger Sensitivity slider (1.0-5.0)
  - Neutrality Suppression slider (0.0-1.0)
  - Real-time calibration updates during active sessions
- **Session Management:**
  - One-click session start/stop
  - Live session duration and frame count tracking
  - Automatic session ID generation
- **Analytics Reports:**
  - Comprehensive clinical assessment page
  - Distress and stability scores
  - Therapeutic recommendations
  - Average emotional profile visualization
  - Longitudinal emotion arc for session review
- **Professional UI:**
  - Tailwind CSS responsive design
  - Mobile-friendly interface
  - Dark mode compatible
  - Loading states and error handling

**Technology Stack:**
- Next.js 14 (App Router)
- TypeScript for type safety
- Zustand for state management
- Axios for API communication
- Recharts for data visualization
- Lucide React for icons

### 2. **Streamlit Dashboard** (Quick Demos & Clinical Validation) 🚀

Rapid deployment option perfect for demonstrations and clinical prototype testing.

**Features:**
- **One-Command Launch:** `streamlit run streamlit_app/dashboard.py`
- **Real-Time Affective Analytics:**
  - Live video feed with emotion overlays
  - Haar Cascade face detection boxes
  - Confidence scores for detected emotions
- **Calibration Panel:**
  - Sadness, Anger, and Neutrality sensitivity controls
  - Instant calibration updates
  - Visual feedback on adjustments
- **Session Controls:**
  - 10-minute timed sessions
  - Manual stop with report generation
  - Reset functionality
- **Therapeutic Analytics Report:**
  - Average emotional profile bar chart
  - Longitudinal session arc line chart
  - Clinical assessment summary
  - Cognitive shift detection (high surprise levels)
  - Distress vs. Stability analysis
  - Therapeutic recommendations
- **Clinical-Ready Features:**
  - CLAHE preprocessing for lighting compensation
  - Temporal smoothing (8-frame buffer) to prevent flickering
  - Yellow clinical light mitigation
  - Muscle tension detection compensation

**Technology Stack:**
- Streamlit for rapid UI development
- Pandas for data analysis
- Matplotlib/Plotly for visualization
- Shared backend core modules

### Architecture Benefits

**Shared Core Engine:**
Both implementations use identical backend modules:
- `backend/core/model.py` - ImprovedCNNEmotion architecture
- `backend/core/inference.py` - Emotion inference engine
- `backend/core/preprocessing.py` - CLAHE + Haar Cascade pipeline
- `backend/services/analytics_engine.py` - Clinical assessment generation

**This ensures:**
✅ Consistent emotion detection results across platforms
✅ Single source of truth for ML model
✅ Easy maintenance and updates
✅ Code reusability

### When to Use Each Dashboard

| Feature | Next.js Dashboard | Streamlit Dashboard |
|---------|-------------------|---------------------|
| **Use Case** | Production deployment | Demos & prototypes |
| **Setup Time** | 5 minutes | 30 seconds |
| **Customization** | Highly customizable | Limited customization |
| **Performance** | Optimized with React | Good for demos |
| **Mobile Support** | ✅ Fully responsive | ⚠️ Basic |
| **API Access** | ✅ Full REST API | ❌ Standalone |
| **Integration** | ✅ Easy to integrate | ⚠️ Limited |
| **Deployment** | Vercel, AWS, etc. | Streamlit Cloud |
| **Best For** | Clinical settings, research | Quick tests, demos |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+ (for Next.js frontend)
- Webcam for real-time emotion detection

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/AI-Emotion-Monitor-HFU.git
cd AI-Emotion-Monitor-HFU
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env to configure your setup (model path, device, etc.)
```

### Running the Applications

#### Option 1: Streamlit Dashboard (Quickest - 30 seconds)

Perfect for quick demos and clinical validation testing.

```bash
# Single command to launch
streamlit run streamlit_app/dashboard.py
```

**Access:** Open browser to `http://localhost:8501`

**Usage:**
1. Adjust calibration sliders (optional)
2. Click "▶️ Start 10-Min Session"
3. Allow webcam access
4. Watch real-time emotion detection
5. Click "⏹️ End & Generate Report"
6. View therapeutic analytics

#### Option 2: Flask API + Next.js Dashboard (Production)

Full-featured professional deployment with REST API backend.

**Terminal 1 - Start Flask API Backend:**
```bash
cd backend
python -m api.app
```
✅ API runs on `http://localhost:5000`
✅ Health check: `curl http://localhost:5000/api/health`

**Terminal 2 - Start Next.js Frontend:**
```bash
cd frontend
npm install  # Only needed first time
npm run dev
```
✅ Dashboard available at `http://localhost:3000`

**Usage:**
1. Open `http://localhost:3000` in browser
2. Adjust calibration sensitivity (optional)
3. Click "Start Session"
4. Allow webcam permissions
5. Real-time emotion detection begins automatically
6. Monitor emotion trends in live charts
7. Click "Stop Session & Generate Report"
8. Automatically redirected to analytics page with clinical assessment

**Pro Tip:** For detailed step-by-step instructions, see `QUICKSTART.md`

---

## 📁 Project Structure

```
AI-Emotion-Monitor-HFU/
├── backend/                          # Flask API & Shared Backend Modules
│   ├── api/
│   │   ├── app.py                    # Flask application initialization
│   │   └── routes/
│   │       ├── emotion.py            # POST /detect, POST /stream
│   │       ├── session.py            # POST /start, POST /stop/:id
│   │       └── analytics.py          # GET /summary/:id, GET /timeseries/:id
│   ├── core/                         # Core ML Modules (Shared)
│   │   ├── model.py                  # ImprovedCNNEmotion architecture
│   │   ├── inference.py              # EmotionInferenceEngine class
│   │   └── preprocessing.py          # CLAHE, Haar Cascade, transforms
│   ├── services/                     # Business Logic
│   │   ├── session_manager.py        # Session state & UUID management
│   │   └── analytics_engine.py       # Clinical assessment generation
│   ├── utils/
│   │   └── config.py                 # Environment configuration
│   └── requirements.txt              # Backend Python dependencies
│
├── frontend/                         # Next.js Dashboard (Production)
│   ├── src/
│   │   ├── lib/
│   │   │   ├── types.ts              # TypeScript type definitions
│   │   │   ├── api.ts                # API client with axios
│   │   │   └── store.ts              # Zustand global state
│   │   ├── hooks/
│   │   │   ├── useSession.ts         # Session management hook
│   │   │   └── useEmotionStream.ts   # Webcam streaming hook
│   │   └── components/
│   │       ├── video/
│   │       │   └── VideoStream.tsx   # Webcam + emotion overlay
│   │       ├── charts/
│   │       │   ├── EmotionBarChart.tsx    # Real-time bar chart
│   │       │   └── TimeSeriesChart.tsx    # Timeline line chart
│   │       └── controls/
│   │           └── CalibrationPanel.tsx   # Session controls & sliders
│   ├── app/
│   │   ├── layout.tsx                # Root layout
│   │   ├── page.tsx                  # Main dashboard page
│   │   ├── globals.css               # Global styles
│   │   └── analytics/
│   │       └── [sessionId]/
│   │           └── page.tsx          # Analytics report page
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.js            # Tailwind CSS config
│   ├── .env.local                    # Frontend environment vars
│   └── README.md                     # Frontend documentation
│
├── streamlit_app/                    # Streamlit Dashboard (Quick Demos)
│   ├── dashboard.py                  # Main Streamlit application
│   └── requirements.txt              # Streamlit dependencies
│
├── models/                           # ML Model Weights
│   └── emotion_model_cnn_improved.pth  # Trained CNN (4.8 MB)
│
├── notebooks/                        # Training & Research
│   └── Group_7_AI_Emotion_Detection_DL.ipynb
│
├── .env.example                      # Environment variable template
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Root Python dependencies
├── README.md                         # This file
├── QUICKSTART.md                     # Detailed setup guide
├── NEXTJS_SETUP.md                   # Next.js implementation details
└── LICENSE                           # Project license
```

**Key Directories:**
- **`backend/`** - All Python backend code (Flask API + shared ML modules)
- **`frontend/`** - Complete Next.js TypeScript application
- **`streamlit_app/`** - Standalone Streamlit dashboard
- **`models/`** - Trained PyTorch model weights
- **`notebooks/`** - Jupyter notebooks for training

---

## 🔌 Flask REST API Documentation

The Flask backend provides a comprehensive REST API for emotion detection, session management, and analytics.

### Base URL
```
http://localhost:5000/api
```

### Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true,
  "device": "cpu"
}
```

### Emotion Detection Endpoints

#### Detect Emotion (Single Frame)
```bash
POST /emotion/detect
Content-Type: multipart/form-data

Body: file=<image_file>
```

**Response:**
```json
{
  "emotion_probs": {
    "Angry": 0.05,
    "Disgust": 0.02,
    "Fear": 0.03,
    "Happy": 0.75,
    "Neutral": 0.10,
    "Sad": 0.02,
    "Surprise": 0.03
  },
  "dominant_emotion": "Happy",
  "confidence": 0.75,
  "faces": [[120, 80, 200, 200]],
  "num_faces": 1
}
```

#### Stream Emotion Frame (With Session Context)
```bash
POST /emotion/stream
Content-Type: application/json

{
  "session_id": "abc123...",
  "image": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "emotion_probs": {...},
  "dominant_emotion": "Happy",
  "confidence": 0.75,
  "faces": [[120, 80, 200, 200]],
  "num_faces": 1,
  "timestamp": 12.5
}
```

#### Get Emotion Labels
```bash
GET /emotion/emotions
```

**Response:**
```json
{
  "emotions": ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
}
```

### Session Management Endpoints

#### Start Session
```bash
POST /session/start
Content-Type: application/json

{
  "calibration": {
    "sad_boost": 2.5,
    "anger_boost": 2.0,
    "neutral_suppress": 0.3
  }
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "start_time": "2026-03-16T12:00:00",
  "is_active": true,
  "calibration": {...},
  "duration_seconds": 0.0,
  "num_frames": 0
}
```

#### Stop Session
```bash
POST /session/stop/<session_id>
```

#### Get Session Details
```bash
GET /session/<session_id>
```

#### Update Calibration
```bash
PUT /session/<session_id>/calibration
Content-Type: application/json

{
  "sad_boost": 3.0,
  "anger_boost": 2.5,
  "neutral_suppress": 0.4
}
```

#### Get Active Sessions
```bash
GET /session/active
```

#### Delete Session
```bash
DELETE /session/<session_id>
```

### Analytics Endpoints

#### Get Clinical Assessment Summary
```bash
GET /analytics/summary/<session_id>
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "duration_seconds": 600.0,
  "num_frames": 3600,
  "avg_emotions": {
    "Angry": 0.05,
    "Happy": 0.65,
    ...
  },
  "distress_score": 0.15,
  "stability_score": 0.75,
  "assessment": {
    "summary": "High Emotional Stability Detected (75%)",
    "level": "success",
    "details": [...],
    "recommendations": [...]
  }
}
```

#### Get Emotion Time-Series
```bash
GET /analytics/timeseries/<session_id>?window_size=30
```

**Response:**
```json
{
  "session_id": "...",
  "timestamps": [0.0, 0.16, 0.33, ...],
  "emotions": [
    {"Angry": 0.05, "Happy": 0.70, ...},
    {"Angry": 0.04, "Happy": 0.72, ...},
    ...
  ]
}
```

#### Get Emotion Distribution
```bash
GET /analytics/distribution/<session_id>
```

**Response:**
```json
{
  "session_id": "...",
  "distribution": {
    "Happy": 2100,
    "Neutral": 1000,
    "Sad": 300,
    ...
  },
  "total_frames": 3600
}
```

#### Get Emotion Variability
```bash
GET /analytics/variability/<session_id>
```

**Response:**
```json
{
  "session_id": "...",
  "variability": {
    "Angry": 0.05,
    "Happy": 0.12,
    ...
  }
}
```

### Example Usage with cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Start session
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"calibration": {"sad_boost": 2.5}}'

# Detect emotion in image
curl -X POST http://localhost:5000/api/emotion/detect \
  -F "file=@face_image.jpg"

# Get analytics
curl http://localhost:5000/api/analytics/summary/abc123
```

---

## ✨ Key Features

### Real-Time Emotion Detection
- **7 Emotion Classes:** Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise
- **Face Detection:** Haar Cascade-based real-time face detection
- **Preprocessing:** CLAHE for lighting normalization (handles clinical yellow lights)
- **Temporal Smoothing:** 8-frame probability buffer prevents label flickering
- **Frame Rate:** 6 FPS for optimal performance/accuracy balance

### Clinical Calibration
- **Sadness Sensitivity:** Adjustable boost (1.0-5.0x) for individual baselines
- **Anger Sensitivity:** Adjustable boost (1.0-5.0x) for stress detection
- **Neutrality Suppression:** Reduce neutral detection (0.0-1.0) for active monitoring
- **Real-time Updates:** Changes applied instantly during active sessions
- **Yellow Light Compensation:** CLAHE preprocessing handles poor clinical lighting

### Session Management
- **UUID-based Tracking:** Unique session IDs for data organization
- **Duration Tracking:** Automatic session timing
- **Frame Counting:** Total frames analyzed per session
- **History Storage:** In-memory emotion probability history
- **State Management:** Active/inactive session states

### Analytics & Reports
- **Distress Score:** Sum of negative emotions (Angry, Disgust, Fear, Sad)
- **Stability Score:** Sum of positive/neutral emotions (Happy, Neutral)
- **Clinical Assessment:** Automated therapeutic evaluation
- **Cognitive Shift Detection:** High surprise levels indicate moments of realization
- **Recommendations:** Contextual therapeutic suggestions
- **Visualizations:**
  - Average emotional profile (bar chart)
  - Longitudinal emotion arc (line chart)
  - Time-series trends with smoothing

### Data Visualization
- **Real-time Charts:** Live updating emotion probability displays
- **Color-Coded:** Red for distress emotions, green for positive
- **Interactive:** Hover tooltips with percentage values
- **Responsive:** Mobile-friendly chart rendering
- **Export Ready:** Session data accessible via API

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **PyTorch 2.0+** - Deep learning framework
- **OpenCV** - Computer vision and face detection
- **Flask 3.0+** - REST API framework
- **Flask-CORS** - Cross-origin resource sharing
- **NumPy** - Numerical computing
- **Pandas** - Data analysis
- **python-dotenv** - Environment configuration

### Frontend (Next.js)
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **React 18** - UI library
- **Tailwind CSS** - Utility-first styling
- **Recharts** - React chart library
- **Zustand** - Lightweight state management
- **Axios** - Promise-based HTTP client
- **Lucide React** - Icon library

### Frontend (Streamlit)
- **Streamlit** - Rapid app development framework
- **Matplotlib/Plotly** - Data visualization

### Machine Learning
- **Model:** Custom Improved CNN
- **Input:** 48x48 grayscale images
- **Architecture:** 4 conv blocks (32→64→128→256 channels)
- **Training:** FER2013 dataset
- **Accuracy:** 65.9% on test set
- **Feature Extraction:** Double convolution blocks with BatchNorm
- **Regularization:** Progressive dropout, Global Average Pooling

---

## 📊 Dashboard Features Comparison

| Feature | Next.js Dashboard | Streamlit Dashboard |
|---------|-------------------|---------------------|
| **Setup** | 5 min (2 terminals) | 30 sec (1 command) |
| **UI/UX** | Modern, professional | Simple, functional |
| **Customization** | Highly customizable | Limited |
| **Real-time Video** | ✅ 6 FPS with overlays | ✅ Variable FPS |
| **Emotion Charts** | ✅ Bar + Line (Recharts) | ✅ Bar + Line (built-in) |
| **Calibration** | ✅ Real-time sliders | ✅ Real-time sliders |
| **Session Management** | ✅ Full CRUD via API | ✅ Start/Stop only |
| **Analytics Page** | ✅ Dedicated page | ✅ Inline report |
| **Mobile Support** | ✅ Fully responsive | ⚠️ Basic |
| **API Access** | ✅ Full REST API | ❌ Standalone |
| **State Management** | ✅ Zustand | ✅ Session state |
| **Type Safety** | ✅ TypeScript | ❌ Python |
| **Error Handling** | ✅ Comprehensive | ✅ Basic |
| **Loading States** | ✅ Yes | ✅ Yes |
| **Export Data** | ✅ Via API endpoints | ⚠️ Manual |
| **Integration** | ✅ Easy to integrate | ⚠️ Limited |
| **Deployment** | Vercel, AWS, Docker | Streamlit Cloud |
| **Best For** | Production, research | Demos, prototypes |
| **Learning Curve** | Medium | Low |

---

## 🧪 Testing the System

### 1. Test Flask API
```bash
# Health check
curl http://localhost:5000/api/health

# Expected: {"status":"healthy","version":"1.0.0",...}

# Get emotion labels
curl http://localhost:5000/api/emotion/emotions

# Expected: {"emotions":["Angry","Disgust",...]}
```

### 2. Test Next.js Dashboard
1. Open `http://localhost:3000`
2. Click "Start Session"
3. Should see: Green success message with session ID
4. Allow webcam permissions
5. Video should appear with "LIVE" indicator
6. Emotion charts should update in real-time

### 3. Test Streamlit Dashboard
1. Open `http://localhost:8501`
2. Adjust calibration sliders (optional)
3. Click "▶️ Start 10-Min Session"
4. Allow webcam permissions
5. Video should appear with emotion overlay
6. Click "⏹️ End & Generate Report"
7. Should see analytics report with charts

### 4. Test Session Workflow
```bash
# Start session via API
curl -X POST http://localhost:5000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"calibration":{"sad_boost":2.5}}'

# Save session_id from response

# Get session details
curl http://localhost:5000/api/session/<session_id>

# Stop session
curl -X POST http://localhost:5000/api/session/stop/<session_id>

# Get analytics
curl http://localhost:5000/api/analytics/summary/<session_id>
```

---

## 🐛 Troubleshooting

### Flask Backend Issues

**"Model file not found"**
```bash
# Check model exists
ls -lh models/emotion_model_cnn_improved.pth

# Should show ~4.8MB file
# If missing, ensure model was moved from root to models/
```

**"Port 5000 already in use"**
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or use different port in .env
echo "API_PORT=5001" >> .env
```

**"CORS error in browser console"**
- Check `.env` has `CORS_ORIGINS=http://localhost:3000`
- Restart Flask API after changing `.env`
- Verify Flask-CORS is installed: `pip show flask-cors`

### Next.js Frontend Issues

**"Cannot connect to API"**
```bash
# 1. Verify Flask is running
curl http://localhost:5000/api/health

# 2. Check frontend .env.local
cat frontend/.env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:5000/api

# 3. Check browser console (F12) for specific error
```

**"Module not found" errors**
```bash
cd frontend
rm -rf node_modules package-lock.json .next
npm install
npm run dev
```

**"Port 3000 in use"**
```bash
lsof -ti:3000 | xargs kill -9
```

### Webcam Issues

**"Permission denied"**
- Check browser camera settings (chrome://settings/content/camera)
- Allow camera access for localhost
- Try different browser (Chrome recommended)
- Restart browser after granting permissions

**"No video feed / black screen"**
- Wait 2-3 seconds for initialization
- Check if another app is using webcam (Zoom, Skype, etc.)
- Refresh the page
- Check browser console for errors

**"No face detected" warning**
- Ensure face is centered in frame
- Improve lighting (face should be well-lit)
- Move closer to camera
- Remove obstructions (glasses may interfere with Haar Cascade)

### Streamlit Issues

**"Streamlit not found"**
```bash
pip install -r streamlit_app/requirements.txt
```

**"Cannot access webcam"**
- Streamlit requires webcam permissions
- Run on main thread (not in background)
- Close other apps using webcam

### Performance Issues

**"Slow inference / low FPS"**
```bash
# Option 1: Enable GPU (if available)
# Install CUDA-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Update .env
echo "DEVICE=cuda" >> .env

# Option 2: Reduce frame rate
# Edit frontend/src/hooks/useEmotionStream.ts
# Change: frameRate: 6 to frameRate: 4
```

**"High memory usage"**
- Reduce smoothing window in config (default: 8 frames)
- Clear session history more frequently
- Use smaller batch sizes

---

## 📝 Configuration

### Environment Variables (.env)

```bash
# Model Configuration
MODEL_PATH=./models/emotion_model_cnn_improved.pth
DEVICE=cpu  # or 'cuda' for GPU

# Flask API
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=true
CORS_ORIGINS=http://localhost:3000

# Inference Settings
ENABLE_SMOOTHING=true
SMOOTHING_WINDOW=8
ENABLE_CALIBRATION=true

# Default Calibration
DEFAULT_SAD_BOOST=2.5
DEFAULT_ANGER_BOOST=2.0
DEFAULT_NEUTRAL_SUPPRESS=0.3

# Session Settings
SESSION_TIMEOUT_MINUTES=60
MAX_ACTIVE_SESSIONS=100
```

### Frontend Configuration (frontend/.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

---

## 🚀 Deployment

### Deploy Flask Backend

**Option 1: Docker**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ ./backend/
COPY models/ ./models/
COPY .env .

CMD ["python", "-m", "backend.api.app"]
```

```bash
docker build -t emotion-monitor-api .
docker run -p 5000:5000 emotion-monitor-api
```

**Option 2: Heroku**
```bash
heroku create emotion-monitor-api
git push heroku main
```

**Option 3: AWS EC2**
- Launch EC2 instance (t2.medium or larger)
- Install Python and dependencies
- Run with Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 backend.api.app:create_app()`

### Deploy Next.js Frontend

**Option 1: Vercel (Recommended)**
```bash
cd frontend
vercel deploy
```

**Option 2: Docker**
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

CMD ["npm", "start"]
```

**Option 3: Static Export**
```bash
npm run build
npm run export
# Deploy 'out/' directory to any static host
```

### Deploy Streamlit

**Streamlit Cloud:**
1. Push to GitHub
2. Connect at share.streamlit.io
3. Select `streamlit_app/dashboard.py`

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 Documentation

- **`README.md`** - This file (project overview)
- **`QUICKSTART.md`** - Detailed step-by-step setup guide
- **`NEXTJS_SETUP.md`** - Next.js component implementation details
- **`frontend/README.md`** - Frontend-specific documentation
- **`backend/API.md`** - Full API specification (to be created)

---

## 🚀 Future Enhancements & Roadmap

While 65.9% is a strong academic benchmark for the FER2013 dataset, the system **requires further optimization** to reach clinical-grade reliability. Future iterations will focus on:

### Model Improvements
* **Hyperparameter Tuning:** Refining dropout rates and learning schedules to minimize generalization error
* **Data Augmentation:** Increasing dataset diversity to handle varied facial orientations and occlusions
* **Transformer Architectures:** Exploring **Vision Transformers (ViTs)** for more nuanced global feature extraction
* **Ensemble Methods:** Combining multiple models for improved accuracy
* **Fine-tuning:** Domain adaptation for specific clinical environments

### Feature Enhancements
* **Multi-Face Tracking:** Monitor multiple patients simultaneously
* **Audio Analysis:** Integrate voice emotion recognition for multimodal detection
* **Historical Comparison:** Compare current session with past sessions
* **Export Functionality:**
  - PDF report generation
  - CSV data export
  - Session video recording
* **Alert System:** Real-time notifications for distress detection
* **Authentication:** User accounts for clinicians and patients
* **Database Integration:** PostgreSQL/MongoDB for persistent storage
* **Offline Mode:** Local storage for areas with poor connectivity

### Infrastructure
* **WebSocket Support:** Bi-directional real-time communication
* **Redis Integration:** Distributed session management
* **Kubernetes Deployment:** Container orchestration for scaling
* **GPU Optimization:** CUDA-accelerated inference
* **Edge Deployment:** Run on local devices for privacy
* **Mobile Apps:** iOS/Android native applications

### Clinical Features
* **Patient Profiles:** Store individual calibration settings
* **Longitudinal Studies:** Multi-session trend analysis
* **Baseline Establishment:** Automatic calibration from initial sessions
* **Integration:** EMR/EHR system connectivity
* **Compliance:** HIPAA/GDPR compliance features
* **Teletherapy:** Remote session monitoring capabilities

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **HFU (Hochschule Furtwangen University)** for academic support
- **FER2013 Dataset** for training data
- **PyTorch Team** for the deep learning framework
- **OpenCV Community** for computer vision tools
- **Streamlit & Next.js Teams** for excellent frameworks

---

## 📧 Contact & Support

For questions, issues, or contributions:

- **Issues:** Open an issue on GitHub
- **Email:** [Your contact information]
- **Documentation:** See `QUICKSTART.md` and `NEXTJS_SETUP.md`

---

## 🎯 Quick Links

- 📘 **[QUICKSTART.md](QUICKSTART.md)** - Detailed setup guide
- 🏗️ **[NEXTJS_SETUP.md](NEXTJS_SETUP.md)** - Next.js implementation details
- 📱 **[frontend/README.md](frontend/README.md)** - Frontend documentation
- 🔬 **[Jupyter Notebook](Group_7_AI_Emotion_Detection_DL.ipynb)** - Model training details

---

**Built with ❤️ for mental health professionals**

*Disclaimer: This system is a research prototype and should not be used as a sole diagnostic tool. Always consult qualified mental health professionals for clinical decisions.*
