import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()


def research_company(company_name: str) -> dict:
    """Research a company using Claude with web search enabled."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""Research the company "{company_name}" thoroughly using web search.

Return ONLY a valid JSON object with exactly these keys:
- summary: one paragraph describing what the company does, who they serve, and their business model
- tech_stack: list of technologies, tools, or platforms they use or build with
- recent_news: list of up to 4 recent notable events, launches, or announcements
- strategic_priorities: list of up to 4 things the company is clearly focused on right now
- interview_questions: list of exactly 3 smart, specific questions a candidate should ask in an interview
- culture_notes: one paragraph describing their work culture, values, or team environment

Do not include any text outside the JSON object. No markdown, no backticks, no explanation."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )
    
    text_content = ""
    for block in response.content:
        if hasattr(block, "text"):
            text_content += block.text
    
    text_content = text_content.strip()
    if text_content.startswith("```"):
        text_content = text_content.split("```", 1)[1]
    
    lines = text_content.split('\n')
    if lines[0].strip().lower() in ('json', 'python', ''):
        text_content = '\n'.join(lines[1:])
    
    if text_content.endswith("```"):
        text_content = text_content.rsplit("```", 1)[0]
    
    text_content = text_content.strip()
    
    try:
        return json.loads(text_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Claude response as JSON: {e}")
