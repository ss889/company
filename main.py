from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone
import os

import claude
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


@app.post("/brief")
async def generate_briefing(request: BriefRequest):
    """Generate a company briefing and save to history."""
    # Validate company_name
    if not request.company_name or not request.company_name.strip():
        raise HTTPException(status_code=400, detail={"error": "company_name is required"})
    
    company_name = request.company_name.strip()
    
    # Research the company
    briefing = claude.research_company(company_name)
    
    # Create a history entry
    entry = {
        "id": uuid.uuid4().hex[:8],
        "company_name": company_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "briefing": briefing
    }
    
    # Save to history
    history = storage.load_history()
    history.append(entry)
    storage.save_history(history)
    
    return entry


@app.get("/history")
async def get_history():
    """Get all search history, most recent first."""
    history = storage.load_history()
    # Reverse to show most recent first
    return list(reversed(history))


@app.delete("/history/{entry_id}")
async def delete_history_entry(entry_id: str):
    """Delete a history entry by id."""
    deleted = storage.delete_entry_by_id(entry_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail={"error": "entry not found"})
    
    return {"message": "deleted"}


# Mount static folder to serve index.html at root
# This must be mounted last to avoid conflicts with other routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
