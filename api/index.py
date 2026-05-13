from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone
import os
import json

from claude import research_company
import storage

app = FastAPI()

# Add CORSMiddleware allowing all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BriefRequest(BaseModel):
    company_name: str


@app.post("/api/brief")
async def generate_briefing(request: BriefRequest):
    """Generate a company briefing and save to history."""
    if not request.company_name or not request.company_name.strip():
        raise HTTPException(status_code=400, detail={"error": "company_name is required"})
    
    company_name = request.company_name.strip()
    
    briefing = research_company(company_name)
    
    entry = {
        "id": uuid.uuid4().hex[:8],
        "company_name": company_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "briefing": briefing
    }
    
    history = storage.load_history()
    history.append(entry)
    storage.save_history(history)
    
    return entry


@app.get("/api/history")
async def get_history():
    """Get all search history, most recent first."""
    history = storage.load_history()
    return list(reversed(history))


@app.delete("/api/history/{entry_id}")
async def delete_history_entry(entry_id: str):
    """Delete a history entry by id."""
    deleted = storage.delete_entry_by_id(entry_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail={"error": "entry not found"})
    
    return {"message": "deleted"}


@app.get("/")
async def root():
    """Serve index.html from public folder."""
    public_path = os.path.join(os.path.dirname(__file__), "..", "public", "index.html")
    if os.path.exists(public_path):
        return FileResponse(public_path)
    return {"message": "Welcome to Company Intelligence API"}
