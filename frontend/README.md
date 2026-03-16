# Next.js Frontend for AI Emotion Monitor

Modern React-based dashboard for real-time emotion detection and clinical monitoring.

## Features

✅ Real-time webcam emotion detection
✅ Live emotion probability visualization
✅ Time-series emotion tracking
✅ Clinical calibration controls
✅ Session management
✅ Therapeutic analytics reports
✅ Responsive design with Tailwind CSS
✅ TypeScript for type safety
✅ Zustand for state management

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Zustand** - Lightweight state management
- **Axios** - HTTP client for API calls
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Flask backend running at `http://localhost:5000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
# .env.local already created with:
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

3. Run development server:
```bash
npm run dev
```

4. Open browser:
```
http://localhost:3000
```

## Project Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── types.ts          # TypeScript type definitions
│   │   ├── api.ts            # API client
│   │   └── store.ts          # Zustand global state
│   ├── hooks/
│   │   ├── useSession.ts     # Session management hook
│   │   └── useEmotionStream.ts  # Webcam streaming hook
│   └── components/
│       ├── video/
│       │   └── VideoStream.tsx     # Webcam video component
│       ├── charts/
│       │   ├── EmotionBarChart.tsx  # Current emotion bar chart
│       │   └── TimeSeriesChart.tsx  # Emotion timeline
│       └── controls/
│           └── CalibrationPanel.tsx  # Session controls & calibration
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Main dashboard
│   ├── globals.css          # Global styles
│   └── analytics/
│       └── [sessionId]/
│           └── page.tsx     # Analytics report page
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## Usage

### Starting a Session

1. Open the dashboard at `http://localhost:3000`
2. Adjust calibration settings (optional):
   - **Sadness Sensitivity** (1.0-5.0) - Adjust detection sensitivity for sadness
   - **Anger Sensitivity** (1.0-5.0) - Adjust detection sensitivity for anger
   - **Neutrality Suppression** (0.0-1.0) - Reduce neutral emotion detection
3. Click **"Start Session"**
4. Allow webcam access when prompted
5. Position your face in the camera frame
6. Emotion detection begins automatically

### During a Session

- View real-time emotion detection in the video feed
- Monitor current emotion probabilities in the bar chart
- Track emotion trends over time in the line chart
- Adjust calibration settings in real-time if needed

### Ending a Session

1. Click **"Stop Session & Generate Report"**
2. Automatically redirected to analytics page
3. Or click **"View Analytics Report"** button in header

### Viewing Analytics

The analytics page shows:
- Session duration and frames analyzed
- Distress and stability scores
- Clinical assessment with recommendations
- Average emotional profile (bar chart)
- Longitudinal emotion arc (line chart)

## API Integration

The frontend connects to the Flask backend at `http://localhost:5000/api`.

### Key API Endpoints Used:

- `POST /session/start` - Create new session
- `POST /session/stop/:id` - End session
- `POST /emotion/stream` - Process video frames
- `PUT /session/:id/calibration` - Update calibration
- `GET /analytics/summary/:id` - Get clinical assessment
- `GET /analytics/timeseries/:id` - Get emotion time-series

## Components Overview

### VideoStream
- Accesses users webcam
- Captures frames at 6 FPS
- Sends frames to backend API
- Displays emotion overlays
- Shows live/streaming indicator

### EmotionBarChart
- Real-time emotion probability visualization
- Color-coded bars for each emotion
- Shows dominant emotion and confidence

### TimeSeriesChart
- Line chart of emotion trends over time
- Tracks 5 key emotions (Angry, Sad, Happy, Neutral, Surprise)
- Shows up to 100 recent data points

### CalibrationPanel
- Calibration sliders for sensitivity adjustment
- Session start/stop controls
- Reset data button
- Session info display

## Customization

### Adjusting Frame Rate
Edit `src/hooks/useEmotionStream.ts`:
```typescript
frameRate: 6,  // Change to desired FPS (1-10 recommended)
```

### Changing Emotions Displayed
Edit `src/components/charts/TimeSeriesChart.tsx`:
```typescript
emotionsToShow = ['Angry', 'Sad', 'Happy', 'Neutral', 'Surprise']
```

### Styling
All styles use Tailwind CSS. Customize in `tailwind.config.js` and component files.

## Troubleshooting

### Webcam Not Working
- Ensure you allowed camera permissions
- Check if another app is using the webcam
- Try refreshing the page
- Webcam only works on HTTPS or localhost

### API Connection Errors
1. Verify Flask backend is running:
   ```bash
   curl http://localhost:5000/api/health
   ```
2. Check `.env.local` has correct API URL
3. Ensure CORS is configured in Flask backend

### Build Errors
```bash
# Clear cache and reinstall
rm -rf .next node_modules package-lock.json
npm install
npm run dev
```

## Production Build

```bash
npm run build
npm run start
```

Or deploy to Vercel:
```bash
vercel deploy
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

See root LICENSE file.
