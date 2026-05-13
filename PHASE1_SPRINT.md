# PHASE 1 SPRINT PLANNING DOCUMENT

---

## SPRINT OVERVIEW

**Goal:** Restructure Company Intelligence platform into an interview-focused intelligence assistant.

**Duration:** 2-3 days (estimated 6-8 hours development + 2-3 hours QA)

**Deliverables:**
- Redesigned sidebar
- Loading state with progress messaging
- Restructured briefing output (6 sections)
- Source attribution
- All tests passing

---

## FILE STRUCTURE (POST-IMPLEMENTATION)

```
project/
├── main.py                    (UPDATED - error handling)
├── claude.py                  (UPDATED - new prompt structure)
├── storage.py                 (NO CHANGE)
├── static/
│   ├── index.html            (MAJOR REWRITE - sidebar + new sections)
│   └── styles.css            (NEW FILE - sidebar styling, skeletons)
├── tests/
│   ├── test_api.py           (UPDATED - new data structure tests)
│   └── test_ui.md            (NEW FILE - UI checklist)
├── PHASE1_FEATURE_SPEC.md    (REFERENCE)
├── PHASE1_SPEC_QA.md         (REFERENCE)
└── PHASE1_SPRINT.md          (THIS FILE)
```

---

## TASK BREAKDOWN

### TASK 1: Update Claude Prompt for Expanded Output
**Owner:** Backend
**Duration:** 1 hour
**Risk:** HIGH (complex prompt engineering)

#### What Changes
`claude.py` — research_company() function

#### Current Prompt Output
```json
{
  "summary": "...",
  "tech_stack": [...],
  "recent_news": [...],
  "strategic_priorities": [...],
  "interview_questions": [...],
  "culture_notes": "..."
}
```

#### New Prompt Output
```json
{
  "snapshot": {
    "tagline": "...",
    "headquarters": "...",
    "industry": "...",
    "founded": 2025,
    "size": "100-500"
  },
  "business_model": {
    "revenue_model": "...",
    "target_customers": "...",
    "pricing": "...",
    "concentration": "..."
  },
  "tech_stack": {
    "frontend": [...],
    "backend": [...],
    "cloud": [...],
    "databases": [...],
    "tools": [...]
  },
  "recent_news": [
    {
      "title": "...",
      "source": "...",
      "date": "2025-03-15",
      "link": "...",
      "summary": "..."
    }
  ],
  "interview_intelligence": {
    "engineering_focus_areas": [...],
    "behavioral_themes": [...],
    "maturity_indicators": "...",
    "culture_notes": "...",
    "preparation_tips": [...]
  },
  "risk_watchlist": {
    "layoffs": "...",
    "funding": "...",
    "competition": "...",
    "product": "...",
    "legal": "..."
  }
}
```

#### Prompt Text Changes
**Old prompt length:** ~300 tokens
**New prompt length:** ~600-700 tokens

**New Prompt Structure:**
```python
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

IMPORTANT:
- Return ONLY valid JSON, no markdown, no backticks
- All fields required (use null or "Unknown" if no data)
- Dates in YYYY-MM-DD format
- Be specific to this company, not generic"""
```

#### Acceptance Criteria
✅ Response includes all 6 top-level fields
✅ No JSON parsing errors
✅ All nested fields are present (even if "Unknown")
✅ Snapshot has company facts, not company story
✅ Interview Intelligence is specific (not generic tips)
✅ News items have dates and sources
✅ Risk section is factual only

---

### TASK 2: Update Data Model (Storage & History)
**Owner:** Backend
**Duration:** 30 minutes
**Risk:** LOW (backward compatible)

#### Changes
`storage.py` — add migration logic for existing briefings

#### What to Do
Add function to handle old vs new schema:
```python
def normalize_briefing(entry):
    """Convert old schema to new schema if needed"""
    if "briefing" in entry:
        briefing = entry["briefing"]
        # If old schema (has 'summary'), migrate to new
        if "summary" in briefing and "snapshot" not in briefing:
            # Keep old fields as-is
            # New generations will have new fields
            pass
    return entry
```

#### Acceptance Criteria
✅ Old briefings in history.json still load without errors
✅ New briefings have expanded structure
✅ No data loss when loading old briefings
✅ No breaking changes to storage.py

---

### TASK 3: Rewrite HTML/CSS for Sidebar Layout
**Owner:** Frontend
**Duration:** 2 hours
**Risk:** MEDIUM (major layout change)

#### File Changes
`static/index.html` — complete restructure

#### Current Layout
```
┌─────────────────────────────────┐
│    Search Panel (top)           │
├─────────────────────────────────┤
│                                 │
│    Briefing Output (main)       │
│                                 │
└─────────────────────────────────┘
```

#### New Layout
```
┌──────────────┬──────────────────┐
│              │                  │
│   Sidebar    │   Briefing       │
│   (sticky)   │   Output         │
│              │                  │
│ • Search     │                  │
│ • Recent     │   (scrollable)   │
│ • Actions    │                  │
│              │                  │
└──────────────┴──────────────────┘
```

#### CSS Changes Required
1. Main grid layout (sidebar + content)
2. Sidebar styling (card-based sections)
3. Skeleton loaders (animated placeholders)
4. Responsive behavior (<768px = collapse/tabs)
5. Sticky positioning for sidebar
6. Card styling for new briefing sections

#### HTML Structure Changes
**OLD:**
```html
<div class="search-section">
  <!-- input, button -->
</div>
<div class="briefing-section">
  <!-- briefing content -->
</div>
```

**NEW:**
```html
<div class="container">
  <aside class="sidebar">
    <div class="search-section">...</div>
    <div class="recent-section">...</div>
    <div class="actions-section">...</div>
  </aside>
  
  <main class="briefing-container">
    <div class="briefing-section">
      <!-- all new sections: snapshot, business_model, etc. -->
    </div>
  </main>
</div>
```

#### Acceptance Criteria
✅ Sidebar displays on left, visible always
✅ Briefing on right, scrolls independently
✅ Two-column layout on desktop (>768px)
✅ Single-column on mobile (<768px)
✅ Dark theme maintained
✅ All existing sections render correctly
✅ New sections (Snapshot, Business Model, etc.) styled consistently

---

### TASK 4: Create New Briefing Sections (HTML Components)
**Owner:** Frontend
**Duration:** 1.5 hours
**Risk:** LOW (straightforward HTML)

#### Sections to Add

**A. Snapshot Section**
```html
<div class="briefing-item snapshot">
  <div class="snapshot-grid">
    <div class="snapshot-field">
      <label>Headquarters</label>
      <value>${headquarters}</value>
    </div>
    <div class="snapshot-field">
      <label>Industry</label>
      <value>${industry}</value>
    </div>
    <div class="snapshot-field">
      <label>Founded</label>
      <value>${founded}</value>
    </div>
    <div class="snapshot-field">
      <label>Size</label>
      <value>${size}</value>
    </div>
  </div>
</div>
```

**B. Business Model Section**
```html
<div class="briefing-item business-model">
  <h3>BUSINESS MODEL</h3>
  <div class="model-grid">
    <div><strong>Revenue:</strong> ${revenue_model}</div>
    <div><strong>Customers:</strong> ${target_customers}</div>
    <div><strong>Pricing:</strong> ${pricing}</div>
    <div><strong>Concentration:</strong> ${concentration}</div>
  </div>
</div>
```

**C. Interview Intelligence Section** (NEW CENTERPIECE)
```html
<div class="briefing-item interview-intelligence">
  <h3>INTERVIEW INTELLIGENCE</h3>
  
  <div class="intelligence-subsection">
    <h4>Engineering Focus Areas</h4>
    <ul class="briefing-list">
      ${engineering_focus_areas.map(item => `<li>${item}</li>`).join('')}
    </ul>
  </div>
  
  <div class="intelligence-subsection">
    <h4>Behavioral Themes</h4>
    <ul class="briefing-list">
      ${behavioral_themes.map(item => `<li>${item}</li>`).join('')}
    </ul>
  </div>
  
  <div class="intelligence-subsection">
    <h4>Company Maturity</h4>
    <p>${maturity_indicators}</p>
  </div>
  
  <div class="intelligence-subsection">
    <h4>Culture & Values</h4>
    <p>${culture_notes}</p>
  </div>
  
  <div class="intelligence-subsection">
    <h4>Preparation Tips</h4>
    <ol class="briefing-list">
      ${preparation_tips.map(tip => `<li>${tip}</li>`).join('')}
    </ol>
  </div>
</div>
```

**D. Risk & Watchlist Section** (NEW)
```html
<div class="briefing-item risk-watchlist">
  <h3>RISK & WATCHLIST</h3>
  <div class="risk-grid">
    <div class="risk-item">
      <label>Layoffs</label>
      <value>${layoffs}</value>
    </div>
    <div class="risk-item">
      <label>Funding</label>
      <value>${funding}</value>
    </div>
    <div class="risk-item">
      <label>Competition</label>
      <value>${competition}</value>
    </div>
    <div class="risk-item">
      <label>Product</label>
      <value>${product}</value>
    </div>
    <div class="risk-item">
      <label>Legal</label>
      <value>${legal}</value>
    </div>
  </div>
</div>
```

#### Acceptance Criteria
✅ All 6 sections render with data from Claude
✅ Styling consistent with existing design
✅ Subsections clearly separated
✅ Lists are properly formatted
✅ Text is readable and scannable
✅ No missing data causes render errors

---

### TASK 5: Implement Loading States & Skeletons
**Owner:** Frontend
**Duration:** 1.5 hours
**Risk:** MEDIUM (animation timing)

#### What to Implement

**A. Skeleton Loader HTML**
```html
<div class="skeleton-loader">
  <div class="skeleton-bar skeleton-heading"></div>
  <div class="skeleton-bar"></div>
  <div class="skeleton-bar"></div>
  <div class="skeleton-section">
    <div class="skeleton-bar"></div>
    <div class="skeleton-bar"></div>
  </div>
</div>
```

**B. Skeleton CSS**
```css
.skeleton-loader {
  padding: 20px;
}

.skeleton-bar {
  height: 16px;
  background: linear-gradient(90deg, #2a2a2a 25%, #3a3a3a 50%, #2a2a2a 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s infinite;
  margin-bottom: 12px;
  border-radius: 4px;
}

.skeleton-heading {
  height: 24px;
  margin-bottom: 20px;
}

.skeleton-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #2a2a2a;
}

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

**C. Progress Message Rotation**
```javascript
const loadingMessages = [
  "Gathering company intelligence…",
  "Analyzing technology stack…",
  "Summarizing recent news…",
  "Identifying key interview topics…",
  "Compiling risk factors…"
];

let messageIndex = 0;
const messageInterval = setInterval(() => {
  const msg = loadingMessages[messageIndex % loadingMessages.length];
  document.getElementById('progressMessage').textContent = msg;
  messageIndex++;
}, 1500);

// Clear on complete
// clearInterval(messageInterval);
```

#### Acceptance Criteria
✅ Skeleton loaders appear while generating
✅ Progress messages rotate every 1.5 seconds
✅ Loading state persists until response received
✅ Animations are smooth (no jank)
✅ Messages are professional/non-distracting

---

### TASK 6: Update News Display with Sources
**Owner:** Frontend
**Duration:** 45 minutes
**Risk:** LOW

#### Changes
Modify news section to display source, date, and link.

#### Current Format
```html
<ul class="briefing-list" id="recentNews"></ul>
```

#### New Format
```html
<div class="news-list" id="recentNews">
  <!-- Each item: -->
  <div class="news-item">
    <h4 class="news-title">${title}</h4>
    <div class="news-meta">
      <span class="news-source">${source}</span>
      <span class="news-date">${date}</span>
    </div>
    <p class="news-summary">${summary}</p>
    ${link ? `<a href="${link}" target="_blank" class="news-link">Read more →</a>` : ''}
  </div>
</div>
```

#### CSS Updates
```css
.news-item {
  padding: 16px;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  margin-bottom: 12px;
}

.news-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #888;
  margin-top: 8px;
}

.news-source {
  background-color: #1a3a3a;
  padding: 2px 8px;
  border-radius: 3px;
}

.news-link {
  color: #4a9eff;
  text-decoration: none;
  font-size: 12px;
  margin-top: 8px;
  display: inline-block;
}
```

#### Acceptance Criteria
✅ Each news item shows title, source, date
✅ Links are clickable and open in new tab
✅ Styling is consistent with design
✅ Dates are readable format (e.g., "Mar 15, 2025")

---

### TASK 7: Add Source Attribution & Timestamps
**Owner:** Frontend
**Duration:** 45 minutes
**Risk:** LOW

#### What to Add

**A. Briefing Header with Timestamp**
```html
<div class="briefing-header">
  <h2 id="companyName"></h2>
  <div class="briefing-meta">
    Generated on <time id="generatedTime"></time>
  </div>
</div>
```

**B. AI Disclosure Footer**
```html
<div class="ai-disclosure">
  <p>
    <strong>About this briefing:</strong> 
    This intelligence is AI-generated from public sources via web search. 
    Always verify critical information independently. 
    <a href="/about" class="disclosure-link">Learn more</a>
  </p>
</div>
```

#### JavaScript Updates
```javascript
function displayBriefing(companyName, briefing) {
  // ... existing code ...
  
  // Add timestamp
  const now = new Date();
  document.getElementById('generatedTime').textContent = 
    now.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
}
```

#### CSS
```css
.briefing-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #2a2a2a;
}

.briefing-meta {
  font-size: 12px;
  color: #888;
  margin-top: 8px;
}

.ai-disclosure {
  margin-top: 40px;
  padding: 16px;
  background-color: #0a1a2a;
  border: 1px solid #1a3a4a;
  border-radius: 6px;
  font-size: 12px;
  color: #888;
}

.ai-disclosure a {
  color: #4a9eff;
  text-decoration: none;
}
```

#### Acceptance Criteria
✅ Timestamp displays in readable format
✅ AI disclosure visible at bottom
✅ Information is clear and not alarmist
✅ Design is subtle and professional

---

### TASK 8: Sidebar Sections (Search, Recent, Actions)
**Owner:** Frontend
**Duration:** 1.5 hours
**Risk:** LOW

#### A. Search Section
```html
<div class="sidebar-section search-section">
  <h3>Search</h3>
  <input 
    type="text" 
    class="search-input" 
    id="companyInput"
    placeholder="e.g. Google, Accel Learning"
  >
  <button class="search-button" id="searchBtn">Generate Briefing</button>
  <div class="progress-message" id="progressMessage"></div>
</div>
```

#### B. Recent Searches Section
```html
<div class="sidebar-section recent-section">
  <h3>Recent Searches</h3>
  <ul class="recent-list" id="recentList">
    <div class="empty-state">No searches yet</div>
  </ul>
</div>
```

#### C. Actions Section
```html
<div class="sidebar-section actions-section">
  <button class="action-btn" id="saveBtn">Save Briefing</button>
  <button class="action-btn" id="exportBtn">Export as PDF</button>
  <button class="action-btn" id="refreshBtn">Refresh Intelligence</button>
</div>
```

#### Sidebar CSS
```css
.sidebar {
  width: 280px;
  padding: 20px;
  background-color: #0f0f0f;
  border-right: 1px solid #2a2a2a;
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow-y: auto;
}

.sidebar-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #2a2a2a;
}

.sidebar-section:last-child {
  border-bottom: none;
}

.sidebar-section h3 {
  font-size: 12px;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 12px;
  font-weight: 700;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  background-color: #1a1a1a;
  border: 1px solid #333;
  border-radius: 4px;
  color: #e0e0e0;
  font-size: 14px;
  margin-bottom: 8px;
}

.search-button {
  width: 100%;
  padding: 10px;
  background-color: #4a9eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}

.search-button:disabled {
  background-color: #2a5a99;
  cursor: not-allowed;
}

.recent-list {
  list-style: none;
  padding: 0;
}

.recent-item {
  padding: 8px 0;
  font-size: 13px;
  cursor: pointer;
  color: #4a9eff;
}

.recent-item:hover {
  text-decoration: underline;
}

.action-btn {
  width: 100%;
  padding: 8px 12px;
  background-color: #2a4a6a;
  color: #4a9eff;
  border: 1px solid #4a9eff;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  margin-bottom: 8px;
}

.action-btn:hover {
  background-color: #3a5a7a;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    max-height: 150px;
    border-right: none;
    border-bottom: 1px solid #2a2a2a;
    position: relative;
    overflow-x: auto;
    display: flex;
    gap: 20px;
  }
  
  .sidebar-section {
    min-width: 200px;
    border-bottom: none;
    margin-bottom: 0;
  }
}
```

#### Acceptance Criteria
✅ Sidebar renders on left side
✅ Sticky positioning keeps sidebar visible while scrolling
✅ All sections visible (Search, Recent, Actions)
✅ Mobile collapses to horizontal/tabs
✅ No layout shift when loading

---

### TASK 9: Update JavaScript Event Handlers
**Owner:** Frontend
**Duration:** 1 hour
**Risk:** MEDIUM (complex state management)

#### Changes Needed

**A. Search Handler**
```javascript
searchBtn.addEventListener('click', async function() {
  const company = searchInput.value.trim();
  if (!company) {
    showError('Please enter a company name');
    return;
  }

  // Show skeleton loader
  briefingSection.innerHTML = '<div class="skeleton-loader">...</div>';
  briefingSection.classList.add('show');
  
  searchBtn.disabled = true;
  searchBtn.textContent = 'Researching...';
  
  // Rotate progress messages
  let msgIndex = 0;
  const msgInterval = setInterval(() => {
    const msg = loadingMessages[msgIndex % loadingMessages.length];
    document.getElementById('progressMessage').textContent = msg;
    msgIndex++;
  }, 1500);

  try {
    const response = await fetch('/brief', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_name: company })
    });

    if (!response.ok) {
      throw new Error('Failed to generate briefing');
    }

    const entry = await response.json();
    clearInterval(msgInterval);
    displayBriefing(entry.company_name, entry.briefing);
    loadHistory();
  } catch (err) {
    showError('Error: ' + err.message);
  } finally {
    searchBtn.disabled = false;
    searchBtn.textContent = 'Generate Briefing';
  }
});
```

**B. Display Briefing Handler**
Update to display all new sections (snapshot, business_model, interview_intelligence, risk_watchlist)

**C. Refresh Button**
```javascript
document.getElementById('refreshBtn').addEventListener('click', async function() {
  const company = document.getElementById('companyName').textContent;
  if (company) {
    searchInput.value = company;
    searchBtn.click();
  }
});
```

**D. Save Button (disabled for Phase 1)**
```javascript
document.getElementById('saveBtn').addEventListener('click', function() {
  alert('Save feature coming soon! (Phase 2)');
});
```

**E. Export Button (disabled for Phase 1)**
```javascript
document.getElementById('exportBtn').addEventListener('click', function() {
  alert('Export feature coming soon! (Phase 2)');
});
```

#### Acceptance Criteria
✅ All event listeners attached
✅ No JavaScript errors in console
✅ Progress messages rotate while generating
✅ Skeleton loaders appear/disappear correctly
✅ All new sections display with correct data

---

### TASK 10: Update API Error Handling
**Owner:** Backend
**Duration:** 30 minutes
**Risk:** LOW

#### Changes
`main.py` — already done, but verify:

```python
@app.post("/brief")
async def generate_briefing(request: BriefRequest):
    if not request.company_name or not request.company_name.strip():
        raise HTTPException(status_code=400, detail={"error": "company_name is required"})
    
    company_name = request.company_name.strip()
    
    try:
        briefing = claude.research_company(company_name)
    except ValueError as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": f"Failed to research: {str(e)}"})
    
    # ... rest of function
```

#### Acceptance Criteria
✅ API errors return proper HTTP status codes
✅ Error messages are user-friendly
✅ No 500 errors without explanation
✅ Invalid company names return 400

---

### TASK 11: Update Tests
**Owner:** QA
**Duration:** 1.5 hours
**Risk:** LOW

#### Test Updates Needed

**A. test_api.py Updates**
- Test new data structure (snapshot, business_model, etc.)
- Mock new fields in FAKE_BRIEFING
- Verify all sections present in response

**B. test_ui.md (NEW - Manual QA Checklist)**
```markdown
# Phase 1 UI Testing Checklist

## Sidebar
- [ ] Sidebar displays on left side
- [ ] Search input visible
- [ ] Generate Briefing button visible
- [ ] Recent Searches section visible
- [ ] Actions section visible

## Loading State
- [ ] "Researching..." button state appears
- [ ] Skeleton loaders visible while generating
- [ ] Progress messages rotate
- [ ] Takes 10-30 seconds (realistic feedback)

## Output Sections
- [ ] Snapshot section displays all 4 fields
- [ ] Business Model section displays
- [ ] Tech Stack categorized (frontend/backend/cloud/db/tools)
- [ ] Recent News shows source + date
- [ ] Interview Intelligence section prominent
- [ ] Risk Watchlist section displays

## Source Attribution
- [ ] Generation timestamp displays
- [ ] AI disclosure visible at bottom
- [ ] News sources are real (not made up)

## Interactions
- [ ] Search new company from sidebar
- [ ] Click recent search reloads briefing
- [ ] Delete recent search removes it
- [ ] Refresh button regenerates same company

## Mobile
- [ ] Sidebar responsive on <768px
- [ ] Briefing readable on mobile
- [ ] No horizontal scroll

## Visual Design
- [ ] Dark theme maintained
- [ ] Typography hierarchy clear
- [ ] Spacing consistent
- [ ] No overlapping elements
- [ ] Professional appearance
```

#### Acceptance Criteria
✅ All unit tests passing
✅ New data structure tests added
✅ Manual QA checklist complete
✅ No console errors

---

## IMPLEMENTATION ORDER

### Day 1 (Frontend Foundation)
1. ✅ Task 3 — Rewrite HTML/CSS for sidebar (2h)
2. ✅ Task 8 — Sidebar sections (1.5h)
3. ✅ Task 4 — New briefing sections (1.5h)
4. **Total: 5 hours**

### Day 2 (Backend + Polish)
1. ✅ Task 1 — Update Claude prompt (1h)
2. ✅ Task 5 — Loading states & skeletons (1.5h)
3. ✅ Task 6 — News display with sources (45min)
4. ✅ Task 7 — Timestamps & disclosure (45min)
5. ✅ Task 9 — JavaScript handlers (1h)
6. **Total: 5 hours**

### Day 3 (QA & Polish)
1. ✅ Task 2 — Data model (30min)
2. ✅ Task 10 — Error handling (30min)
3. ✅ Task 11 — Tests & manual QA (2h)
4. **Total: 3 hours**

**Total Estimate: 13 hours (3 full days)**

---

## DEPENDENCIES & BLOCKERS

**Hard Dependencies:**
- Claude API working (existing, verified ✅)
- Fetch API working (existing, verified ✅)

**Soft Dependencies:**
- None

**Known Risks:**
- Claude prompt engineering (new prompt structure, higher complexity)
- Skeleton animations (CSS must be smooth, no jank)
- Mobile responsiveness (sidebar reorganization)

---

## READY FOR IMPLEMENTATION?

**✅ YES**

All tasks are clearly defined with:
- Specific file changes
- HTML/CSS code snippets
- JavaScript examples
- Acceptance criteria
- Risk levels
- Time estimates

**Next Step:** Approve sprint plan and begin implementation.

