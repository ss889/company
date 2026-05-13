# PHASE 1 FEATURE SPECIFICATION

Company Intelligence Platform — Restructure for Interview Preparation Focus

---

## OVERVIEW

Transform the application from a static briefing tool into a dynamic interview preparation assistant by restructuring the UX layout, improving user feedback during generation, and enriching the output information architecture.

---

## PHASE 1 GOALS

✅ Sidebar redesign (persistent control center)
✅ Loading states with progress messaging
✅ Output restructuring (clearer, role-relevant sections)
✅ Interview Intelligence section (new centerpiece)
✅ Source attribution & transparency

---

# FEATURE 1: SIDEBAR REDESIGN

## Current State
- Simple input box + button at top
- Empty after generation
- Passive user experience

## Target State
- Persistent left sidebar (always visible)
- Divided into sections: Search, Recent, Actions
- Functional control center

### A. SEARCH SECTION

**Requirements:**
- Company name input field
- "Generate Briefing" button
- Loading state: button shows "Researching..." + disabled
- Loading indicator visible while generating

**Acceptance Criteria:**
- Input remains visible and functional after generation
- Can search for new company without losing current briefing
- Loading state lasts for entire generation duration (visually communicates work)

### B. RECENT SEARCHES SECTION

**Requirements:**
- Display list of previous searches
- Each item shows: company name + timestamp
- Clickable to reload that briefing
- Delete button per item
- Empty state: "No searches yet"

**Acceptance Criteria:**
- Recent searches persist across sessions (via history.json)
- Click on past search instantly loads that briefing
- Delete removes from history
- Max 10 visible (scroll if more)

### C. ACTIONS SECTION

**Requirements:**
- Button: "Save Briefing" (bookmarks current briefing locally)
- Button: "Export as PDF" (generate PDF of briefing)
- Button: "Refresh Intelligence" (re-run same company)

**Acceptance Criteria:**
- Save creates a separate saved.json file
- Export uses jsPDF or similar to create downloadable PDF
- Refresh shows loading state, regenerates briefing

---

## SIDEBAR LAYOUT

```
┌─────────────────────────────┐
│    COMPANY INTELLIGENCE     │
├─────────────────────────────┤
│ Search Section              │
│ ├─ Input: Company Name      │
│ └─ Button: Generate         │
├─────────────────────────────┤
│ Recent Searches             │
│ ├─ Google (May 13, 2:30 PM) │
│ ├─ Giftogram (May 13)       │
│ └─ [Accel] (May 12)         │
├─────────────────────────────┤
│ Actions                     │
│ ├─ Save Briefing            │
│ ├─ Export as PDF            │
│ └─ Refresh Intelligence     │
└─────────────────────────────┘
```

---

# FEATURE 2: LOADING STATES & PROGRESS MESSAGING

## Current State
Button shows "Researching..." but no progressive feedback.

## Target State
Multi-stage loading with rotating progress messages.

### Requirements

During generation, rotate messages every 1-2 seconds:
1. "Gathering company intelligence…"
2. "Analyzing technology stack…"
3. "Summarizing recent news…"
4. "Identifying key interview topics…"
5. "Compiling risk factors…"

**Visual Treatment:**
- Skeleton loaders in briefing area (placeholder blocks)
- Rotating progress text below button
- Subtle pulse animation on skeleton

**Acceptance Criteria:**
- Messages rotate while generating
- Skeletons show before real content loads
- Animation is professional, not distracting
- Loading state prevents multiple simultaneous requests

---

# FEATURE 3: OUTPUT RESTRUCTURING

## Current Sections
- Company Name
- Overview (dense paragraph)
- Tech Stack
- Recent News
- Strategic Priorities
- Interview Questions
- Culture Notes

## Target Sections (RESTRUCTURED)

### A. COMPANY SNAPSHOT (NEW)
**Purpose:** Quick reference facts about the company.

**Content:**
- Company name (large heading)
- 1-sentence tagline
- Headquarters
- Industry/Sector
- Founded year
- Approximate size (employees)

**Data Source:** Claude generates from prompt

**Acceptance Criteria:**
- Displays in compact card format
- All fields present (estimated from web search results)
- Quick visual scan provides context

### B. BUSINESS MODEL (NEW)
**Purpose:** Explain how the company generates revenue.

**Content:**
- Revenue model (SaaS, marketplace, advertising, etc.)
- Target customers (B2B, B2C, enterprise, SMB)
- Pricing approach
- Customer concentration (if known)

**Data Source:** Claude extracts from web search

**Acceptance Criteria:**
- Concise (2-3 sentences max)
- Explains what they sell and to whom
- Clear to non-business users

### C. TECHNOLOGY STACK (IMPROVED)
**Existing content, enhanced:**

**Improvements:**
- Categorize technologies by type:
  - Frontend
  - Backend
  - Infrastructure/Cloud
  - Databases
  - Tools/SaaS
- Add confidence indicators (if available)
- Expand from current tag format

**Acceptance Criteria:**
- Grouped logically
- Easier to scan by category
- More comprehensive tech list

### D. RECENT NEWS (ENHANCED)
**Existing content, improved:**

**Improvements:**
- Add dates to news items
- Add source attribution (company blog, TechCrunch, etc.)
- Add "Read more" links where possible
- Limit to 4 items (highest impact)

**Acceptance Criteria:**
- Each item has date
- Source visible
- Sorted by recency
- Links are clickable

### E. INTERVIEW INTELLIGENCE (NEW - HIGH PRIORITY)
**Purpose:** Prepare interview candidates for likely topics.

**Content:**
- Engineering Focus Areas (likely technical interview topics based on tech stack)
- Behavioral Themes (based on company culture signals)
- Company Maturity Indicators (startup, scale-up, enterprise)
- Engineering Culture Notes
- Preparation Recommendations (specific things to study/prepare)

**Example Output:**
```
Engineering Focus Areas:
- Cloud infrastructure (AWS/GCP extensive use)
- Microservices architecture (multiple backend services visible)
- Real-time systems (if company uses streaming)
- Security & compliance (if financial/healthcare)

Behavioral Themes:
- Customer obsession (customer-facing founding story)
- Technical depth (emphasis on engineering)
- Execution speed (frequent product updates)

Engineering Maturity:
- Mid-stage growth company (founded 2015)
- Modern tech stack (cloud-native)
- Investment in infrastructure

Preparation Tips:
- Study their public APIs
- Review recent engineering blog posts
- Prepare examples of scalability/performance work
- Be ready to discuss trade-offs in system design
```

**Data Source:** Claude synthesizes from all available intelligence

**Acceptance Criteria:**
- Clearly actionable
- Specific to company (not generic)
- Helps candidate prepare strategically
- 4-5 bullet points per subsection

### F. RISK & WATCHLIST SECTION (NEW)
**Purpose:** Provide realistic assessment of company health/stability.

**Content:**
- Layoffs/Personnel changes (if recent)
- Funding status (latest round, runway health indicators)
- Market competition (primary competitors, threat level)
- Product concerns (market fit signals, pivot indicators)
- Legal/Compliance issues (if public knowledge)

**Example:**
```
Potential Risk Factors:
- Recent layoffs: 5% headcount reduction (Feb 2025)
- Funding: Series C, 18 months runway estimated
- Competition: Market consolidating, 3 major competitors
- Growth: YoY growth slowing to 15% (from 40%)

Strategic Implications:
- Company is profitable-focused (not growth-at-all-costs)
- Hiring may slow
- Interview questions may emphasize efficiency/ROI
```

**Data Source:** Claude extracts from news, announcements, public statements

**Acceptance Criteria:**
- Factual only (no speculation)
- Sourced from public information
- Helpful for decision-making
- Balanced (not sensationalized)

---

# FEATURE 4: SOURCE ATTRIBUTION & TRANSPARENCY

## Current State
Generated intelligence appears authoritative but lacks source info.

## Target State
All information includes transparency about sources and confidence.

### Requirements

#### A. TIMESTAMP
Every briefing shows:
- "Generated on May 13, 2026 at 2:30 PM"
- "Last updated: May 13, 2026"

#### B. NEWS SOURCE ATTRIBUTION
Each news item includes:
- Title
- Source (e.g., "TechCrunch", "Company Blog")
- Date
- [Optional] Link/Read more

#### C. AI DISCLOSURE
Add footer banner:
```
"This briefing is AI-generated from public sources. 
Information is sourced from web search results and may contain inaccuracies. 
Always verify critical information independently."
```

#### D. CONFIDENCE INDICATORS
For sections that have uncertainty, show:
- "Based on public information" (news, funding)
- "Inferred from tech stack" (culture, engineering focus)
- "From company materials" (official sources)

**Acceptance Criteria:**
- Every briefing shows generation timestamp
- News items have sources
- AI disclosure visible but non-intrusive
- Users understand reliability of each section

---

# DATA MODEL CHANGES

## Updated Briefing Entry

```json
{
  "id": "abc123",
  "company_name": "Giftogram",
  "created_at": "2026-05-13T14:30:00Z",
  "last_updated": "2026-05-13T14:30:00Z",
  "briefing": {
    "snapshot": {
      "tagline": "Digital gift card and rewards platform",
      "headquarters": "Parsippany, NJ",
      "industry": "B2B SaaS",
      "founded": 2012,
      "size": "200-500 employees"
    },
    "business_model": {
      "revenue_model": "SaaS subscription + transaction fees",
      "target_customers": "Enterprise companies, mid-market",
      "pricing": "Per-employee-per-month model",
      "concentration": "Diversified across Fortune 500 base"
    },
    "tech_stack": {
      "frontend": ["React", "Vue.js"],
      "backend": ["Python", "Node.js"],
      "cloud": ["AWS", "GCP"],
      "databases": ["PostgreSQL", "Redis"],
      "tools": ["Salesforce", "HubSpot", "Slack"]
    },
    "recent_news": [
      {
        "title": "Giftogram Series B Funding",
        "source": "TechCrunch",
        "date": "2025-03-15",
        "link": "https://techcrunch.com/...",
        "summary": "Raised $50M Series B"
      }
    ],
    "interview_intelligence": {
      "engineering_focus_areas": ["..."],
      "behavioral_themes": ["..."],
      "maturity_indicators": "...",
      "culture_notes": "...",
      "preparation_tips": ["..."]
    },
    "risk_watchlist": {
      "layoffs": "None recent",
      "funding": "Series B, 18 months runway",
      "competition": "Moderate",
      "product": "Stable",
      "legal": "None known"
    },
    "source_attribution": {
      "generated_at": "2026-05-13T14:30:00Z",
      "confidence_notes": "Based on public sources"
    }
  }
}
```

---

# CLAUDE PROMPT CHANGES

Current prompt returns 6 fields. New prompt must return expanded structure.

**New Prompt Requirements:**
- Snapshot (company facts)
- Business Model (revenue, customers)
- Tech Stack (categorized)
- Interview Intelligence (focus areas, behaviors, tips)
- Risk Watchlist (real risks, not speculation)
- Source info (what's public vs inferred)

---

# ACCEPTANCE CRITERIA (PHASE 1)

✅ Sidebar displays and remains visible after generation
✅ Can search new company from sidebar without losing current briefing
✅ Recent searches load instantly when clicked
✅ Loading state shows rotating progress messages for 5-30 seconds
✅ Skeleton loaders appear while generating
✅ Output displays all new sections (Snapshot, Business Model, Interview Intelligence, Risk)
✅ News items show source and date
✅ Briefing shows generation timestamp
✅ AI disclosure visible at bottom
✅ All text content is accurate/factual
✅ No console errors
✅ Mobile responsive (sidebar may collapse)
✅ All links in news are clickable

---

# OUT OF SCOPE (PHASE 1)

❌ Role-specific personalization
❌ Company comparison
❌ PDF export
❌ Save briefings
❌ Advanced analytics
❌ Trend tracking

These are Phase 2 & 3 features.

---

# TECHNICAL NOTES

- Sidebar can be styled CSS Grid
- Loading messages rotate with setInterval (1.5s)
- Skeleton loaders: CSS placeholders or npm skeleton component
- Claude prompt expanded from current ~300 tokens to ~600 tokens
- Response size increases from ~1KB to ~3-4KB
- Generation time may increase from 10s to 20-30s (more content from Claude)

---

# SUCCESS METRIC

After Phase 1, the application should feel like a professional intelligence platform, not a simple AI wrapper. Users should feel guided through interview preparation with structured, actionable insights.
