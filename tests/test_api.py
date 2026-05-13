import pytest
import os
import json
from unittest.mock import patch
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Import the app and modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import storage
from main import app


# Test history file path
TEST_HISTORY_FILE = "test_history.json"


# Fake briefing dict for mocking
FAKE_BRIEFING = {
    "summary": "A fast-moving B2B SaaS platform for employee recognition and incentive management.",
    "tech_stack": ["Python", "React", "PostgreSQL", "Salesforce", "HubSpot"],
    "recent_news": [
        "Raised Series B in March 2025",
        "Launched Slack integration in Q1 2025",
        "Expanded to 50+ enterprise clients"
    ],
    "strategic_priorities": [
        "Expanding enterprise client base",
        "AI-powered personalization of rewards",
        "International market entry"
    ],
    "interview_questions": [
        "How is the team currently using AI to improve the rewards workflow?",
        "What does success look like in the first 90 days for this role?",
        "How do you measure the impact of incentive campaigns for enterprise clients?"
    ],
    "culture_notes": "Fast-moving B2B team, emphasis on ownership and business outcomes. Strong engineering culture with regular feedback cycles."
}


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Set up test environment and clean up after each test."""
    # Override storage file path to test file
    storage.HISTORY_FILE = TEST_HISTORY_FILE
    
    # Clean up before test
    if os.path.exists(TEST_HISTORY_FILE):
        os.remove(TEST_HISTORY_FILE)
    
    yield
    
    # Clean up after test
    if os.path.exists(TEST_HISTORY_FILE):
        os.remove(TEST_HISTORY_FILE)
    
    # Reset to default
    storage.HISTORY_FILE = "history.json"


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@patch("claude.research_company")
def test_generate_briefing(mock_research, client):
    """Test POST /brief with valid company name returns 200 and correct fields."""
    mock_research.return_value = FAKE_BRIEFING
    
    response = client.post("/brief", json={"company_name": "Giftogram"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify entry structure
    assert "id" in data
    assert "company_name" in data
    assert "created_at" in data
    assert "briefing" in data
    
    # Verify briefing content
    assert data["company_name"] == "Giftogram"
    assert data["briefing"]["summary"] == FAKE_BRIEFING["summary"]
    assert data["briefing"]["tech_stack"] == FAKE_BRIEFING["tech_stack"]
    assert data["briefing"]["recent_news"] == FAKE_BRIEFING["recent_news"]
    assert data["briefing"]["strategic_priorities"] == FAKE_BRIEFING["strategic_priorities"]
    assert data["briefing"]["interview_questions"] == FAKE_BRIEFING["interview_questions"]
    assert data["briefing"]["culture_notes"] == FAKE_BRIEFING["culture_notes"]
    
    # Verify it was saved to history
    history = storage.load_history()
    assert len(history) == 1
    assert history[0]["company_name"] == "Giftogram"


@patch("claude.research_company")
def test_generate_briefing_empty_name(mock_research, client):
    """Test POST /brief with empty string returns 400."""
    response = client.post("/brief", json={"company_name": ""})
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data["detail"]


@patch("claude.research_company")
def test_get_history(mock_research, client):
    """Test GET /history returns a list."""
    mock_research.return_value = FAKE_BRIEFING
    
    # Add a couple of entries
    client.post("/brief", json={"company_name": "Company A"})
    client.post("/brief", json={"company_name": "Company B"})
    
    response = client.get("/history")
    
    assert response.status_code == 200
    history = response.json()
    
    # Should be a list
    assert isinstance(history, list)
    assert len(history) == 2
    
    # Should be reverse order (most recent first)
    assert history[0]["company_name"] == "Company B"
    assert history[1]["company_name"] == "Company A"


@patch("claude.research_company")
def test_delete_entry(mock_research, client):
    """Test DELETE /history/{id} removes entry and returns 200."""
    mock_research.return_value = FAKE_BRIEFING
    
    # Add an entry
    create_response = client.post("/brief", json={"company_name": "Giftogram"})
    entry_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/history/{entry_id}")
    
    assert response.status_code == 200
    assert response.json() == {"message": "deleted"}
    
    # Verify it's gone
    history = storage.load_history()
    assert len(history) == 0


@patch("claude.research_company")
def test_delete_nonexistent_entry(mock_research, client):
    """Test DELETE /history/fakeid returns 404."""
    response = client.delete("/history/fakeid")
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data["detail"]
