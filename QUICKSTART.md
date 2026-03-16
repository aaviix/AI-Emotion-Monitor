# 🚀 Quick Start Guide - Flask API + Next.js Dashboard

Complete guide to get your AI Emotion Monitor running in minutes.

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Webcam available
- [ ] Terminal/command line access

## Step 1: Install Python Dependencies

```bash
# Navigate to project root
cd /Users/aaviix/Desktop/PERSONAL/AI-Emotion-Monitor-HFU

# Install Python packages
pip install -r requirements.txt
```

## Step 2: Setup Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# .env is already configured with defaults, no changes needed for local development
```

## Step 3: Start Flask Backend API

Open Terminal 1:

```bash
cd /Users/aaviix/Desktop/PERSONAL/AI-Emotion-Monitor-HFU/backend

# Start Flask API
python -m api.app
```

You should see:
```
Loading emotion inference engine...
============================================================
AI Emotion Monitor Configuration
============================================================
Model Path:          /Users/aaviix/Desktop/PERSONAL/AI-Emotion-Monitor-HFU/models/emotion_model_cnn_improved.pth
Device:              cpu
API Host:            0.0.0.0:5000
...
✓ Emotion inference engine loaded successfully
 * Running on http://0.0.0.0:5000
```

**Test the API:**
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status":"healthy","version":"1.0.0","model_loaded":true,"device":"cpu"}
```

## Step 4: Install Next.js Dependencies

Open Terminal 2:

```bash
cd /Users/aaviix/Desktop/PERSONAL/AI-Emotion-Monitor-HFU/frontend

# Install Node packages
npm install
```

This will take 1-2 minutes to install all dependencies.

## Step 5: Start Next.js Frontend

In Terminal 2 (same window):

```bash
# Start Next.js development server
npm run dev
```

You should see:
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

## Step 6: Open the Dashboard

1. Open your browser
2. Navigate to: `http://localhost:3000`
3. You should see the **AI Emotion Monitor Dashboard**

## Step 7: Start Your First Session

1. **Adjust Calibration** (optional):
   - Sadness Sensitivity: 2.5 (default)
   - Anger Sensitivity: 2.0 (default)
   - Neutrality Suppression: 0.3 (default)

2. **Click "Start Session"**
   - A session ID will be created
   - Flask API will receive the request

3. **Allow Webcam Access**
   - Browser will prompt for camera permissions
   - Click "Allow"

4. **Position Your Face**
   - Center your face in the video frame
   - Emotion detection begins automatically
   - You'll see real-time emotion overlays

5. **Monitor Emotions**
   - Bar chart shows current emotion probabilities
   - Line chart tracks trends over time
   - Calibration panel shows session info

6. **Stop Session**
   - Click "Stop Session & Generate Report"
   - You'll be redirected to the analytics page

## Step 8: View Analytics

The analytics page shows:
- ✅ Session duration and frame count
- ✅ Distress and stability scores
- ✅ Clinical assessment with recommendations
- ✅ Average emotional profile chart
- ✅ Longitudinal emotion timeline

## Alternative: Running Streamlit (Simple Demo)

If you want to quickly test just the Streamlit version:

Terminal 1:
```bash
cd /Users/aaviix/Desktop/PERSONAL/AI-Emotion-Monitor-HFU
streamlit run streamlit_app/dashboard.py
```

Open: `http://localhost:8501`

---

## Troubleshooting

### Flask API Issues

**Port already in use:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Model not found error:**
```bash
# Verify model file exists
ls -lh models/emotion_model_cnn_improved.pth
```

**CORS errors:**
- Check `.env` has `CORS_ORIGINS=http://localhost:3000`
- Restart Flask API after changing `.env`

### Next.js Issues

**Port 3000 in use:**
```bash
# Kill process
lsof -ti:3000 | xargs kill -9
```

**Dependencies issues:**
```bash
cd frontend
rm -rf node_modules package-lock.json .next
npm install
npm run dev
```

**API connection failed:**
1. Verify Flask is running: `curl http://localhost:5000/api/health`
2. Check `.env.local` has correct API URL
3. Open browser DevTools (F12) → Console for errors

### Webcam Issues

**Permission denied:**
- Check browser camera settings
- Allow camera access for localhost
- Restart browser if needed

**No video feed:**
- Ensure no other app is using webcam
- Close Zoom, Skype, etc.
- Try refreshing the page

**Black screen:**
- Wait a few seconds for initialization
- Check browser console for errors
- Try a different browser (Chrome recommended)

---

## Success Checklist

- [ ] Flask API running on http://localhost:5000
- [ ] Health endpoint responds: `curl http://localhost:5000/api/health`
- [ ] Next.js app running on http://localhost:3000
- [ ] Dashboard loads in browser
- [ ] Can start a session
- [ ] Webcam access granted
- [ ] Video feed shows in dashboard
- [ ] Emotions detected in real-time
- [ ] Can stop session and view analytics

---

## Next Steps

### Customize the Dashboard
- Edit calibration defaults in `frontend/src/lib/store.ts`
- Change colors in `frontend/src/lib/types.ts` (EMOTION_COLORS)
- Adjust frame rate in `frontend/src/hooks/useEmotionStream.ts`

### Add Features
- Export session data to CSV/JSON
- Multi-user support with authentication
- Historical session comparison
- Email reports
- Database integration for persistent storage

### Deploy to Production
**Backend:**
- Use Gunicorn or uWSGI for production WSGI server
- Deploy to cloud (AWS, GCP, Heroku)
- Use PostgreSQL/MongoDB for session storage
- Add Redis for caching

**Frontend:**
- Deploy to Vercel: `vercel deploy`
- Or build static: `npm run build && npm run start`
- Configure production API URL in environment

---

## Performance Optimization

**For better model performance:**
1. Install PyTorch with CUDA support (if you have NVIDIA GPU):
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

2. Update `.env`:
   ```
   DEVICE=cuda
   ```

3. Restart Flask API

**Frame rate adjustment:**
- Low-end machines: 4-5 FPS
- Standard machines: 6-7 FPS (default)
- High-end + GPU: 10+ FPS

---

## Support

**Check logs:**
- Flask: Terminal 1 output
- Next.js: Terminal 2 output
- Browser: F12 → Console tab

**Common issues resolved:**
- 90% are CORS/API connection issues → verify Flask is running
- 5% are webcam permission issues → allow camera access
- 5% are dependency issues → reinstall packages

**Still stuck?**
- Check `frontend/README.md` for detailed frontend docs
- Check `NEXTJS_SETUP.md` for component details
- Review Flask logs for backend errors

---

**🎉 Congratulations! Your AI Emotion Monitor is now running!**
