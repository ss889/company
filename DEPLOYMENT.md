# Render.com Deployment Guide

This project is configured for deployment on [Render.com](https://render.com) using traditional Python web services.

## Deployment Steps

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up and log in
- Connect your GitHub account

### 2. Create a Web Service
1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repo: `ss889/company`
3. Configure:
   - **Name:** `company-intelligence`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free (or upgraded based on traffic)

### 3. Add Environment Variable
In the Render dashboard for your web service:

**Environment:**
```
ANTHROPIC_API_KEY = sk-ant-api03-[your-key-already-added]
```

(You mentioned you've already added this, so you're good!)

### 4. Deploy
1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repo
   - Run `pip install -r requirements.txt`
   - Start the FastAPI app with Uvicorn
   - Assign you a public URL

### 5. Access Your App
Your app will be live at:
```
https://company-intelligence.onrender.com
```

(Render gives you a custom subdomain)

## Project Structure for Render

```
project/
├── main.py              # FastAPI app
├── claude.py            # Claude research logic
├── storage.py           # History file management
├── static/
│   └── index.html       # Frontend UI
├── tests/
│   └── test_api.py      # Test suite
├── render.yaml          # Render configuration
├── requirements.txt     # Python dependencies
└── .env                 # Local env (NOT deployed)
```

## Key Differences from Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| Server Type | Traditional (always running) | Serverless |
| Port | Dynamic `$PORT` env var | Fixed paths |
| Storage | Persistent filesystem | Ephemeral (`/tmp/`) |
| Cold Starts | None (server always on) | 5-10 seconds |
| Cost | Free tier available | Pay-as-you-go |

## API Endpoints

Your app will have these endpoints:

- **POST** `/brief` — Generate a company briefing
- **GET** `/history` — Get all saved searches
- **DELETE** `/history/{id}` — Delete a saved search
- **GET** `/` — Serve the frontend

## Local Development

```bash
cd project
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your_key_here"
python -m uvicorn main:app --reload
```

Then visit `http://localhost:8000`

## Troubleshooting

**"ModuleNotFoundError"**
- Check that all imports in main.py are correct
- Verify `requirements.txt` has all dependencies

**"ANTHROPIC_API_KEY not set"**
- Make sure it's added in Render's Environment Variables
- Redeploy after adding it

**"Port already in use"**
- Render uses the `$PORT` environment variable automatically
- Don't hardcode the port in startCommand

**App not starting**
- Check Render's logs (Dashboard → Logs)
- Verify startCommand: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## History Persistence

Unlike Vercel, Render's free tier gives you a persistent filesystem, so search history is stored locally in `history.json` and persists across deployments.

For production with multiple instances, upgrade to use a database service.

