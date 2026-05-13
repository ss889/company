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


# Fake briefing dict for mocking - NEW STRUCTURE (Phase 1)
FAKE_BRIEFING = {
    "snapshot": {
        "tagline": "B2B SaaS for employee recognition and incentive management",
        "headquarters": "San Francisco, CA",
        "industry": "HR Tech / Employee Engagement",
        "founded": 2020,
        "size": "100-200"
    },
    "business_model": {
        "revenue_model": "SaaS subscription",
        "target_customers": "Enterprise and mid-market (50-5000+ employees)",
        "pricing": "Per-employee per-month model, typically $2-8/user",
        "concentration": "Diversified across Fortune 500 and growth companies"
    },
    "tech_stack": {
        "frontend": ["React", "TypeScript", "Tailwind CSS"],
        "backend": ["Python", "Node.js", "Django"],
        "cloud": ["AWS", "Google Cloud"],
        "databases": ["PostgreSQL", "Redis"],
        "tools": ["Salesforce", "Slack", "Stripe", "HubSpot"]
    },
    "recent_news": [
        {
            "title": "Raises $15M Series B funding led by Accel Partners",
            "source": "TechCrunch",
            "date": "2025-03-15",
            "link": "https://techcrunch.com/...",
            "summary": "Giftogram announced Series B funding to expand product and go-to-market efforts."
        },
        {
            "title": "Launches Native Slack Integration",
            "source": "Company Blog",
            "date": "2025-02-20",
            "link": "https://blog.giftogram.com/...",
            "summary": "Users can now manage recognition workflows directly from Slack."
        },
        {
            "title": "Reaches 50+ Enterprise Customers",
            "source": "LinkedIn",
            "date": "2025-01-10",
            "link": "https://linkedin.com/...",
            "summary": "Giftogram celebrates milestone with major enterprises adopting the platform."
        }
    ],
    "interview_intelligence": {
        "engineering_focus_areas": [
            "Scalability and performance at enterprise scale",
            "Real-time notification systems and event streaming",
            "Integration architecture with third-party APIs",
            "Data analytics and reporting infrastructure"
        ],
        "behavioral_themes": [
            "Ownership and accountability in building features",
            "Cross-functional collaboration with product and customer success",
            "Customer-first problem solving and empathy",
            "Continuous learning and staying current with tech trends"
        ],
        "maturity_indicators": "Series B growth stage, rapidly expanding engineering team, focus on scaling and reliability",
        "culture_notes": "High-paced startup culture, emphasis on ownership, transparent communication, customer focus. Regular feedback cycles and professional growth opportunities.",
        "preparation_tips": [
            "Study their recent funding announcement and what they plan to build",
            "Research their product and try the demo or free trial",
            "Prepare examples of scaling systems from your own experience",
            "Think about questions on how they approach cross-functional work",
            "Review their tech stack and why those choices make sense for their use case"
        ],
        "interview_questions": [
            "Design a scalable notification system that delivers recognition updates to thousands of users in real-time across multiple channels (email, Slack, SMS).",
            "How would you approach building integrations with third-party APIs (Salesforce, Slack, HubSpot) while maintaining reliability and security?",
            "Tell us about a time you optimized a slow database query in production. What was your approach?",
            "Describe how you would build and maintain an analytics pipeline to track user engagement metrics across the platform.",
            "Walk us through how you would implement a feature flag system to safely roll out new features to enterprise customers.",
            "How would you ensure data consistency when a recognition is created, processed, and delivered across multiple systems?",
            "What's your experience with event-driven architectures? How would you use them to decouple services?"
        ]
    },
    "risk_watchlist": {
        "layoffs": "None recent",
        "funding": "Series B (March 2025) - strong runway estimated at 24-36 months",
        "competition": "Moderate - competing with Bonusly, HeyTaco, other recognition platforms",
        "product": "Strong product-market fit evidenced by customer growth and enterprise adoption",
        "legal": "No known major legal or compliance issues"
    }
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
    
    # Verify briefing content - NEW STRUCTURE
    assert data["company_name"] == "Giftogram"
    assert "snapshot" in data["briefing"]
    assert data["briefing"]["snapshot"]["headquarters"] == "San Francisco, CA"
    assert "business_model" in data["briefing"]
    assert "tech_stack" in data["briefing"]
    assert "recent_news" in data["briefing"]
    assert "interview_intelligence" in data["briefing"]
    assert "risk_watchlist" in data["briefing"]
    
    # Verify tech_stack has categories
    assert "frontend" in data["briefing"]["tech_stack"]
    assert "backend" in data["briefing"]["tech_stack"]
    
    # Verify news has proper structure
    assert isinstance(data["briefing"]["recent_news"], list)
    if data["briefing"]["recent_news"]:
        assert "title" in data["briefing"]["recent_news"][0]
        assert "source" in data["briefing"]["recent_news"][0]
        assert "date" in data["briefing"]["recent_news"][0]
    
    # Verify interview intelligence is a dict with subsections
    assert "engineering_focus_areas" in data["briefing"]["interview_intelligence"]
    assert "behavioral_themes" in data["briefing"]["interview_intelligence"]
    
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
