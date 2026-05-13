# Deployment Checklist — Phase 1 Live

**Status:** Code pushed to GitHub ✅
**Commit:** 6bbb126
**Next:** Monitor Render deployment

---

## DEPLOYMENT TIMELINE

### ✅ Completed
- [x] All code changes committed (9 files)
- [x] Pushed to GitHub (master branch)
- [x] Render webhook triggered

### ⏳ In Progress
- [ ] Render detects new commit (usually 10-30 seconds)
- [ ] Deployment starts (shows "Building" in dashboard)
- [ ] Dependencies installed
- [ ] Application starts on port $PORT
- [ ] Health check passes

### ⏹ Pending
- [ ] Manual verification on live URL
- [ ] Test with real company search
- [ ] Verify all sections render correctly

---

## WHAT WAS DEPLOYED

**Files Updated:**
- `static/index.html` - New sidebar layout + 6 sections
- `claude.py` - Expanded prompt with new data structure
- `tests/test_api.py` - Updated tests (all passing)

**Files Added:**
- `PHASE1_FEATURE_SPEC.md` - Requirements documentation
- `PHASE1_SPEC_QA.md` - QA verification
- `PHASE1_SPRINT.md` - Sprint planning
- `PHASE1_SPRINT_QA.md` - Sprint QA
- `PHASE1_IMPLEMENTATION_SUMMARY.md` - What was built
- `PHASE1_QA_CHECKLIST.md` - Manual QA checklist

**Unchanged (but verified):**
- `main.py` - FastAPI routes (working correctly)
- `storage.py` - JSON file I/O (working correctly)

---

## VERIFY DEPLOYMENT

### Step 1: Check Render Dashboard
1. Go to https://dashboard.render.com/
2. Find your service (likely "company-intelligence" or similar)
3. Look for:
   - Status: "Live" (green)
   - Latest deploy: Should show commit 6bbb126 recently
   - Logs: Should show successful startup

### Step 2: Monitor Deployment Logs
Expected log output:
```
Building dependencies...
Building image...
Deploying...
[2026-05-13...] Started server process
[2026-05-13...] Uvicorn running on 0.0.0.0:$PORT
```

### Step 3: Test Live URL
1. Get your Render URL: https://your-service.onrender.com/
2. Open in browser
3. Verify:
   - Page loads without errors
   - Sidebar visible on left
   - Recent searches appear (if any exist in history)

---

## LIVE VERIFICATION TASKS

### Functional Testing
1. **Test Search:**
   - Enter company name: "Google"
   - Click "Generate Briefing"
   - Wait for briefing to load (should take 15-30 seconds with Claude API)
   - Verify all sections render

2. **Test Sections:**
   - [ ] Snapshot section shows real data
   - [ ] Business Model section populates
   - [ ] Tech Stack shows technologies
   - [ ] Recent News displays articles with sources
   - [ ] Interview Intelligence shows tips
   - [ ] Risk & Watchlist shows risks

3. **Test Interactions:**
   - [ ] Copy All button works
   - [ ] Search another company
   - [ ] Recent searches list updates
   - [ ] Click recent search loads it

4. **Test Error Handling:**
   - [ ] Empty search shows error
   - [ ] Invalid input shows error
   - [ ] Error clears after 5 seconds

### Responsive Testing
1. Open live URL on mobile device or use DevTools responsive mode
2. Test at 375px width (iPhone SE):
   - [ ] Sidebar transforms to tabs
   - [ ] Content is readable
   - [ ] No horizontal scroll
   - [ ] Buttons are tap-friendly

### Performance Testing
1. Open DevTools (F12)
2. Go to Network tab
3. Do a search and verify:
   - [ ] Request to /brief completes
   - [ ] Response is valid JSON
   - [ ] Response time is reasonable (< 30 seconds including Claude API)
   - [ ] No 4xx or 5xx errors

---

## TROUBLESHOOTING

### If "Service Error" appears
- **Cause:** ANTHROPIC_API_KEY not set or Claude API error
- **Fix:** 
  1. Go to Render dashboard → Service settings
  2. Check Environment Variables
  3. Verify ANTHROPIC_API_KEY is set
  4. Restart service

### If briefing doesn't load
- **Check Browser Console (F12):**
  - Look for JavaScript errors
  - Check Network tab for /brief response
  - Verify response is valid JSON
- **Check Render Logs:**
  - Look for Python errors
  - Check Claude API response

### If sections don't display
- **Check Browser Console for errors**
- **Verify JSON structure matches new format**
- **Check that Claude returned all required fields**

### If styling looks wrong
- **Clear browser cache:** Ctrl+Shift+Delete
- **Do a hard refresh:** Ctrl+Shift+R
- **Check that CSS loaded:** DevTools Network tab → filter "css"

---

## ROLLBACK PLAN (If needed)

If something breaks after deployment:

1. **Quick Fix (if code issue):**
   - Fix the code locally
   - Run tests: `pytest tests/test_api.py -v`
   - Commit and push again

2. **Rollback (if urgent):**
   - Go to Render dashboard
   - Click "Manual Deploy"
   - Select previous commit (069942e)
   - Deploy that version
   - Meanwhile, fix and re-deploy

3. **Check Logs:**
   - Render dashboard → Logs tab
   - Look for error messages
   - Search for stack traces

---

## SUCCESS CRITERIA

Phase 1 is successfully deployed when:
- ✅ Live URL loads without errors
- ✅ Can search for companies
- ✅ Briefing displays all 6 new sections
- ✅ Data is populated from Claude API
- ✅ Sidebar interactions work
- ✅ Responsive on mobile
- ✅ No console errors
- ✅ Copy functionality works

---

## NEXT STEPS AFTER VERIFICATION

Once live deployment is verified:

1. **Share link with team/users**
2. **Monitor Render logs for errors**
3. **Collect user feedback**
4. **Plan Phase 2 features:**
   - Save Briefing (database)
   - Export PDF
   - Search autocomplete
   - Role-based personalization
   - Company comparison

---

## RENDER SERVICE INFO

**Service Type:** Web Service (not serverless)
**Framework:** Python FastAPI
**Language:** Python 3.11
**Web Server:** Uvicorn
**Port:** Dynamic ($PORT environment variable)
**Health Check:** Built-in /docs endpoint
**Logs:** Real-time in Render dashboard
**Auto-deploy:** Enabled (triggers on GitHub push)
**Environment Variables:** Set in Render dashboard
**Database:** JSON file (history.json) - stored locally

---

## DEPLOYMENT COMPLETE

**Commit:** 6bbb126
**Date:** May 13, 2026
**Changes:** 9 files, 3731+ insertions
**Status:** Ready for live verification

Once verified, Phase 1 is officially **PRODUCTION READY**.
