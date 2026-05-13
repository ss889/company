# Company Intelligence Briefing Tool

A tool for job seekers preparing for interviews. Enter a company name, get a structured briefing covering what the company does, their tech stack, recent news, strategic priorities, and smart questions to ask in the interview.

## Setup

### Prerequisites
- Python 3.8+
- Anthropic API key

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure API Key
Edit the `.env` file and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_actual_key_here
```

## Running

Start the server:
```bash
uvicorn main:app --reload
```

Open http://localhost:8000 in your browser.

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## Architecture

- **main.py** — FastAPI application with three routes
- **claude.py** — Claude API integration with web search
- **storage.py** — History file I/O
- **static/index.html** — Frontend UI
- **history.json** — Persistent search history

## Features

- Generate structured company briefings
- View recent searches
- Delete search history
- Copy briefing to clipboard
- Dark theme, responsive design

## Why This Project

**Skill Demonstrated:** Backend API development with FastAPI, live AI web search integration via Claude's web_search tool, and automated testing with pytest.

**Why It Was Built:** The developer went through a job search process requiring 30+ minutes of manual company research per application. This tool automates that into a structured 30-second briefing.

**Connection to Target Role:** Directly maps to AI Operations Manager and AI Solutions Engineer roles that require building AI-powered workflow tools for non-technical teams.

**Technical Interest:** Uses Claude's real-time web search capability to synthesize live data into structured JSON output — not static documents, but live research.
