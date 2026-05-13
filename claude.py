import anthropic
import os
import json
import logging
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Try to load .env file if it exists (local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def research_company(company_name: str) -> dict:
    """Research a company using Ollama or Claude API."""
    
    # Check if Ollama is available (local development)
    use_ollama = os.getenv("USE_OLLAMA", "false").lower() == "true"
    
    if use_ollama:
        return research_company_ollama(company_name)
    else:
        return research_company_anthropic(company_name)


def research_company_ollama(company_name: str) -> dict:
    """Research using Ollama (local, free model)."""
    logger.info(f"Using Ollama to research {company_name}")
    
    # Ollama API endpoint
    url = "http://localhost:11434/api/chat"
    
    prompt = f"""Research the company "{company_name}" thoroughly. Provide detailed information.

Return ONLY a valid JSON object with EXACTLY these fields (use "Unknown" if unavailable, NEVER null):

{{
  "snapshot": {{
    "tagline": "one-line what they do",
    "headquarters": "City, Country",
    "industry": "market category",
    "founded": "YYYY",
    "size": "employee range like 100-500"
  }},
  "business_model": {{
    "revenue_model": "SaaS/marketplace/ads/etc",
    "target_customers": "B2B/B2C/enterprise/SMB",
    "pricing": "how they charge",
    "concentration": "Diversified or specific focus"
  }},
  "tech_stack": {{
    "frontend": ["React", "Vue", "or similar"],
    "backend": ["Python", "Node.js", "or similar"],
    "cloud": ["AWS", "GCP", "or similar"],
    "databases": ["PostgreSQL", "MongoDB", "or similar"],
    "tools": ["Slack", "Salesforce", "or similar"]
  }},
  "recent_news": [
    {{"title": "headline", "source": "TechCrunch", "date": "YYYY-MM-DD", "link": "url or null", "summary": "1-2 sentences"}}
  ],
  "interview_intelligence": {{
    "engineering_focus_areas": ["topic1", "topic2", "topic3", "topic4"],
    "behavioral_themes": ["theme1", "theme2", "theme3", "theme4"],
    "maturity_indicators": "description of company stage",
    "culture_notes": "key cultural indicators",
    "preparation_tips": ["tip1", "tip2", "tip3", "tip4", "tip5"],
    "interview_questions": ["realistic question 1", "realistic question 2", "realistic question 3", "realistic question 4", "realistic question 5", "realistic question 6", "realistic question 7"]
  }},
  "risk_watchlist": {{
    "layoffs": "Recent layoffs or None",
    "funding": "latest round or Profitable",
    "competition": "competitive position",
    "product": "market fit assessment",
    "legal": "legal issues or None known"
  }}
}}

CRITICAL: Return ONLY valid JSON - no markdown, no backticks, no explanation.
Start your response with {{ and end with }}."""
    
    try:
        logger.debug(f"Calling Ollama at {url} with model mistral")
        response = requests.post(url, json={
            "model": "mistral",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        text_content = result.get("message", {}).get("content", "")
        logger.debug(f"Ollama response: {text_content[:300]}...")
        
        # Parse JSON from response
        start_idx = text_content.find('{')
        end_idx = text_content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            text_content = text_content[start_idx:end_idx+1]
        
        briefing = json.loads(text_content)
        return _ensure_all_fields(briefing)
        
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama. Make sure 'ollama serve' is running on localhost:11434")
        raise ValueError("Cannot connect to Ollama. Make sure you've run 'ollama serve' in another terminal.")
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        raise ValueError(f"Failed to research company with Ollama: {e}")


def research_company_anthropic(company_name: str) -> dict:
    """Research using Anthropic Claude API (requires API key)."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    logger.info(f"Using Anthropic Claude to research {company_name}")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Research the company "{company_name}" thoroughly using web search. You MUST provide detailed factual information for each field.

Return ONLY a valid JSON object with EXACTLY these fields (use "Unknown" if unavailable, NEVER null):

{{
  "snapshot": {{
    "tagline": "one-line what they do",
    "headquarters": "City, Country",
    "industry": "market category",
    "founded": "YYYY",
    "size": "employee range like 100-500"
  }},
  "business_model": {{
    "revenue_model": "SaaS/marketplace/ads/etc",
    "target_customers": "B2B/B2C/enterprise/SMB",
    "pricing": "how they charge",
    "concentration": "Diversified or specific focus"
  }},
  "tech_stack": {{
    "frontend": ["React", "Vue", "or similar"],
    "backend": ["Python", "Node.js", "or similar"],
    "cloud": ["AWS", "GCP", "or similar"],
    "databases": ["PostgreSQL", "MongoDB", "or similar"],
    "tools": ["Slack", "Salesforce", "or similar"]
  }},
  "recent_news": [
    {{"title": "headline", "source": "TechCrunch", "date": "YYYY-MM-DD", "link": "url or null", "summary": "1-2 sentences"}}
  ],
  "interview_intelligence": {{
    "engineering_focus_areas": ["topic1", "topic2", "topic3", "topic4"],
    "behavioral_themes": ["theme1", "theme2", "theme3", "theme4"],
    "maturity_indicators": "description of company stage",
    "culture_notes": "key cultural indicators",
    "preparation_tips": ["tip1", "tip2", "tip3", "tip4", "tip5"],
    "interview_questions": ["realistic question 1", "realistic question 2", "realistic question 3", "realistic question 4", "realistic question 5", "realistic question 6", "realistic question 7"]
  }},
  "risk_watchlist": {{
    "layoffs": "Recent layoffs or None",
    "funding": "latest round or Profitable",
    "competition": "competitive position",
    "product": "market fit assessment",
    "legal": "legal issues or None known"
  }}
}}

CRITICAL RULES:
1. Return ONLY valid JSON - no markdown, no backticks, no explanation
2. EVERY field must have a value - use "Unknown" never null
3. Arrays must have at least 3-5 items each
4. For recent_news, include actual recent articles if found
5. Be specific about {company_name} - not generic

Start your response with {{ and end with }}. Nothing else."""

    response = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=3000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract text content from response blocks
    text_content = ""
    for block in response.content:
        if hasattr(block, "text"):
            text_content += block.text
    
    logger.debug(f"Raw Claude response: {text_content[:500]}...")
    
    # Strip markdown backticks and language identifiers
    text_content = text_content.strip()
    
    # Remove markdown code blocks if present
    if text_content.startswith("```"):
        text_content = text_content.lstrip("`")
        # Remove language identifier (json, python, etc.)
        lines = text_content.split('\n', 1)
        if len(lines) > 1 and lines[0].strip().lower() in ('json', 'python', 'text', ''):
            text_content = lines[1]
        text_content = text_content.rstrip("`").strip()
    
    # Find JSON object boundaries
    start_idx = text_content.find('{')
    end_idx = text_content.rfind('}')
    
    if start_idx != -1 and end_idx != -1:
        text_content = text_content[start_idx:end_idx+1]
    
    logger.debug(f"Cleaned JSON: {text_content[:300]}...")
    
    try:
        result = json.loads(text_content)
        return _ensure_all_fields(result)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Failed content: {text_content}")
        raise ValueError(f"Failed to parse Claude response as JSON: {e}")


def _ensure_all_fields(briefing: dict) -> dict:
    """Ensure all required fields exist with proper structure."""
    if 'snapshot' not in briefing:
        briefing['snapshot'] = {}
    if 'business_model' not in briefing:
        briefing['business_model'] = {}
    if 'tech_stack' not in briefing:
        briefing['tech_stack'] = {'frontend': [], 'backend': [], 'cloud': [], 'databases': [], 'tools': []}
    if 'recent_news' not in briefing:
        briefing['recent_news'] = []
    if 'interview_intelligence' not in briefing:
        briefing['interview_intelligence'] = {}
    if 'risk_watchlist' not in briefing:
        briefing['risk_watchlist'] = {}
    return briefing
