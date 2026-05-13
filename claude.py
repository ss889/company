import anthropic
from dotenv import load_dotenv
import os
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()


def research_company(company_name: str) -> dict:
    """Research a company using Claude with web search enabled."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Research the company "{company_name}" thoroughly using web search.

Return ONLY a valid JSON object with these exact fields:

1. SNAPSHOT (company facts):
   - tagline: one-line description of what company does
   - headquarters: city, state/country
   - industry: sector or market category
   - founded: 4-digit year
   - size: approximate employee count (e.g., "200-500")

2. BUSINESS_MODEL:
   - revenue_model: SaaS, marketplace, advertising, etc.
   - target_customers: B2B, B2C, enterprise, SMB, etc.
   - pricing: description of pricing approach
   - concentration: if known, customer concentration (e.g., "Diversified", "Fortune 500-focused")

3. TECH_STACK (categorized):
   - frontend: list of frontend technologies
   - backend: list of backend technologies
   - cloud: list of cloud providers/services
   - databases: list of databases/data stores
   - tools: list of SaaS tools (Salesforce, HubSpot, Slack, etc.)

4. RECENT_NEWS (max 4 items, each with):
   - title: news headline
   - source: where news came from (TechCrunch, Company Blog, etc.)
   - date: YYYY-MM-DD format
   - link: URL if available, else null
   - summary: 1-2 sentence summary

5. INTERVIEW_INTELLIGENCE (predict what they'll ask):
   - engineering_focus_areas: list of likely technical interview topics (max 4)
   - behavioral_themes: list of likely behavioral themes (max 4)
   - maturity_indicators: brief description of company stage
   - culture_notes: key cultural indicators
   - preparation_tips: list of specific things to study (max 5)

6. RISK_WATCHLIST (real, factual risks only):
   - layoffs: "None recent" or description
   - funding: latest funding round, runway if known
   - competition: competitive position
   - product: product market fit indicators
   - legal: any known legal/compliance issues

CRITICAL: Return ONLY valid JSON. No markdown, no backticks, no language identifier, no explanation.
All fields required (use null or "Unknown" if no data available)."""

    response = client.messages.create(
        model="claude-opus-4-1",
        max_tokens=2048,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract text content from response blocks
    text_content = ""
    for block in response.content:
        if hasattr(block, "text"):
            text_content += block.text
    
    # Strip markdown backticks if present
    text_content = text_content.strip()
    if text_content.startswith("```"):
        # Remove opening markdown fence
        text_content = text_content.split("```", 1)[1]
    
    # Strip language identifier (e.g. "json") if present on first line
    lines = text_content.split('\n')
    if lines[0].strip().lower() in ('json', 'python', ''):
        text_content = '\n'.join(lines[1:])
    
    if text_content.endswith("```"):
        # Remove closing markdown fence
        text_content = text_content.rsplit("```", 1)[0]
    
    text_content = text_content.strip()
    
    try:
        return json.loads(text_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Claude response as JSON: {e}")
