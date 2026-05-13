# Vercel Deployment Guide

This project is configured for deployment on Vercel using serverless Python functions.

## Deployment Steps

### 1. Create Vercel Account
- Go to [vercel.com](https://vercel.com)
- Sign up with GitHub (recommended for easy CI/CD)

### 2. Add Environment Variables
Once you connect your GitHub repo to Vercel, add the following environment variable in Vercel's dashboard:

**Settings → Environment Variables:**
```
Name: ANTHROPIC_API_KEY
Value: sk-ant-api03-[your-actual-key-from-anthropic]
```
(Paste your actual Anthropic API key, not this placeholder)

### 3. Deploy
Once you push to GitHub, Vercel will automatically detect the `vercel.json` config and deploy:
- Python FastAPI backend → `/api/` serverless functions
- Static HTML frontend → `public/index.html`
- Automatic builds from requirements.txt

### 4. Access Your App
After deployment, Vercel will give you a URL like:
```
https://your-project-name.vercel.app
```

The app will be fully functional with:
- Frontend at the root (`/`)
- API endpoints at `/api/brief`, `/api/history`, `/api/history/{id}`

## Project Structure for Vercel

```
project/
├── api/
│   ├── index.py          # FastAPI app (main entry point)
│   ├── claude.py         # Claude research logic
│   └── storage.py        # History file management
├── public/
│   └── index.html        # Frontend UI
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── .env                  # Local env (NOT deployed)
```

## Important Notes

- **API Key is NOT in Git** — It's only stored as a Vercel environment variable for security
- **History Storage** — Uses `/tmp/` on Vercel (ephemeral per deployment)
- **Cold Starts** — First request may take 5-10 seconds as the serverless function spins up
- **Max Timeout** — Set to 30 seconds (see `vercel.json`)

## Local Development

For local testing with the Vercel structure:
```bash
cd project
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your_key_here"
uvicorn api.index:app --reload
```

Then visit `http://localhost:8000`

## Troubleshooting

**"ModuleNotFoundError: No module named 'claude'"**
- Vercel runs from the `api/` directory, so imports are correct

**"ANTHROPIC_API_KEY not set"**
- Ensure the env var is added in Vercel dashboard settings
- Redeploy after adding it

**History not persisting**
- Vercel `/tmp/` is ephemeral. For persistent storage, upgrade to use a database service
