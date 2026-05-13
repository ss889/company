# Phase 1 — Day 3 QA CHECKLIST

**Status:** Ready for manual testing and deployment
**Previous Status:** All code complete, all unit tests passing ✅

---

## MANUAL QA CHECKLIST

### A. SIDEBAR FUNCTIONALITY (Desktop)
- [ ] Sidebar visible on left side
- [ ] Sidebar width is appropriate (not too wide, not too narrow)
- [ ] Search input accepts company names
- [ ] "Generate Briefing" button is clickable
- [ ] Progress message displays during generation
- [ ] Recent searches list populates after first search
- [ ] Can click recent search to reload it
- [ ] Delete button appears next to each recent search
- [ ] Delete removes item from list and from history
- [ ] Actions buttons visible (Save, Export, Refresh)
- [ ] Save/Export buttons show "coming in Phase 2" message when clicked
- [ ] Refresh button regenerates current briefing

### B. LOADING STATES (Desktop)
- [ ] Skeleton loaders appear when generating
- [ ] Skeleton animation is smooth (no jank)
- [ ] Progress messages rotate every ~1.5 seconds
- [ ] All 5 progress messages display at least once
- [ ] Messages are professional and not alarming
- [ ] Loading state clears when briefing loads

### C. NEW BRIEFING SECTIONS (Desktop)
- [ ] Company Snapshot section renders with all 4 fields
  - [ ] Headquarters shows city/country
  - [ ] Industry shows market category
  - [ ] Founded shows year
  - [ ] Company Size shows employee count
- [ ] Business Model section renders with all 4 fields
  - [ ] Revenue Model shows type
  - [ ] Target Customers shows market
  - [ ] Pricing shows approach
  - [ ] Customer Concentration shows focus
- [ ] Technology Stack shows categories
  - [ ] Frontend technologies display as chips
  - [ ] Backend technologies display as chips
  - [ ] Cloud technologies display as chips
  - [ ] Databases display as chips
  - [ ] Tools & Services display as chips
- [ ] Recent News section displays
  - [ ] Title is visible
  - [ ] Source badge shows (colored)
  - [ ] Date is readable
  - [ ] Summary paragraph shows
  - [ ] "Read more" link appears if URL present
- [ ] Interview Intelligence section prominent
  - [ ] "Engineering Focus Areas" subsection visible
  - [ ] "Behavioral Themes" subsection visible
  - [ ] "Company Maturity" text displays
  - [ ] "Culture & Values" text displays
  - [ ] "Preparation Tips" list shows
  - [ ] Blue border/background styling applied
- [ ] Risk & Watchlist section visible
  - [ ] Layoffs field shows status
  - [ ] Funding field shows status
  - [ ] Competition field shows status
  - [ ] Product field shows status
  - [ ] Legal field shows status
  - [ ] Red border/background styling applied

### D. SOURCE ATTRIBUTION & TRANSPARENCY (Desktop)
- [ ] Briefing header shows company name
- [ ] Timestamp shows in format "Mon DD, YYYY HH:MM"
- [ ] AI Disclosure footer visible at bottom
- [ ] Disclosure text is clear but not alarmist
- [ ] No confidence scores missing or broken

### E. INTERACTIONS (Desktop)
- [ ] Enter key in search input triggers search
- [ ] Copy All button works
- [ ] Copied text includes all sections
- [ ] "Copied!" feedback shows for 2 seconds
- [ ] Can search multiple companies sequentially
- [ ] Briefing updates when searching new company
- [ ] No console errors when searching

### F. ERROR HANDLING (Desktop)
- [ ] Empty search shows error message
- [ ] Error message disappears after 5 seconds
- [ ] Network error shows helpful message
- [ ] API error (if applicable) shows user-friendly text
- [ ] No 500 error pages or stack traces

### G. RESPONSIVE DESIGN (Mobile)
- [ ] Sidebar transforms to horizontal layout on mobile
- [ ] Main content takes full width
- [ ] Briefing sections stack vertically
- [ ] All text is readable (no tiny fonts)
- [ ] Buttons are tap-friendly (not too small)
- [ ] Sidebar sections are scrollable horizontally
- [ ] No horizontal scroll on main content
- [ ] Snapshot grid becomes single column
- [ ] Tech categories become single column
- [ ] All sections accessible without excessive scrolling

### H. VISUAL DESIGN (Desktop & Mobile)
- [ ] Dark theme (#0f0f0f background) maintained
- [ ] Text contrast is readable (WCAG AA standard)
- [ ] Spacing is consistent (12px, 16px, 20px)
- [ ] Typography hierarchy is clear
- [ ] No overlapping elements
- [ ] Shadows/borders are subtle
- [ ] Blue accent color (#4a9eff) used consistently
- [ ] Red accent color (#ff6b6b) for risks
- [ ] Professional appearance overall

### I. PERFORMANCE
- [ ] Page loads quickly (< 2 seconds)
- [ ] Skeleton animation doesn't slow browser
- [ ] No lag when scrolling briefing
- [ ] Sidebar is sticky without jumps
- [ ] Copy button responds immediately

---

## BROWSER TESTING

### Desktop Browsers
- [ ] Chrome/Edge (latest)
- [ ] Firefox (if available)
- [ ] Safari (if available)

### Mobile Testing
- [ ] Mobile Chrome (Android)
- [ ] Safari (iOS)
- [ ] Any available mobile device

---

## DEPLOYMENT VERIFICATION

### Before Pushing to Render
1. [ ] All manual QA checks pass
2. [ ] No console errors in DevTools
3. [ ] Network tab shows successful /brief and /history calls
4. [ ] history.json file exists and contains entries
5. [ ] All test files still pass: `pytest tests/test_api.py -v`

### Render Deployment Steps
1. [ ] Push code to GitHub (git add, commit, push)
2. [ ] Verify Render detects changes
3. [ ] Check deployment logs for errors
4. [ ] Wait for deployment to complete
5. [ ] Test live URL in browser
6. [ ] Run through manual QA on live URL
7. [ ] Verify ANTHROPIC_API_KEY is set in Render dashboard

### Post-Deployment
1. [ ] Test with real company (Giftogram, Google, etc.)
2. [ ] Verify all sections populate with real data
3. [ ] Check that timestamps are current
4. [ ] Verify news sources are real and relevant
5. [ ] Confirm interview intelligence is specific

---

## SIGN-OFF

### When All Checks Pass
```
✅ Phase 1 QA COMPLETE
✅ Ready for production deployment
✅ All features working as specified
✅ No known issues
```

### If Issues Found
1. Document the issue clearly
2. Note steps to reproduce
3. Flag as blocker or nice-to-have
4. Fix in subsequent task/sprint

---

## TESTING COMPANIES

### Recommended Test Cases
1. **Giftogram** - Known company (existing in history)
2. **Google** - Large well-known company
3. **Anthropic** - AI company (relevant to product)
4. **Render** - Web hosting company (deployment target)
5. **[Your Company]** - Personal interest check

### Expected Output Validation
For each test company:
- [ ] Snapshot has real headquarters
- [ ] Industry is correct
- [ ] Business model matches actual business
- [ ] Tech stack is plausible for company
- [ ] News is recent and real
- [ ] Interview intelligence is specific
- [ ] Risk assessment is factual

---

## KNOWN ISSUES TO IGNORE (Phase 2+)

- Save Briefing button doesn't save (Phase 2)
- Export PDF button doesn't export (Phase 2)
- No search autocomplete (Phase 2)
- No company comparison (Phase 3)
- No role-based personalization (Phase 2)

These are intentionally disabled for Phase 1.

---

## QUICK TROUBLESHOOTING

### Briefing doesn't display
- Check browser console for errors
- Verify Claude API returned valid JSON
- Check that all required fields are present

### Sidebar not sticky on mobile
- Verify media query is working (@media 768px)
- Check browser DevTools responsive mode
- Test on actual mobile device

### Copy button not working
- Verify navigator.clipboard API supported
- Check for HTTPS (clipboard needs secure context)
- Test in different browser

### Progress messages not rotating
- Verify setInterval is running (check console)
- Check that msgIndex is incrementing
- Verify loadingMessages array has 5 items

---

## ESTIMATED QA TIME

- Desktop manual QA: 30-45 minutes
- Mobile manual QA: 15-20 minutes
- Deployment: 5-10 minutes
- Post-deployment testing: 10-15 minutes

**Total: 60-90 minutes**

---

## HAND-OFF

Once all QA checks pass, Phase 1 is officially **COMPLETE** and ready for:
- User feedback
- Phase 2 feature planning
- Performance optimization if needed
- Production monitoring

