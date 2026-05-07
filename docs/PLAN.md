# GiftingGenie v2 — Execution Plan

Companion to `PRD.md`. Task-level breakdown with checkboxes you can tick off.

---

## Phase 0 — Foundation (Week 1)

### 0.1 Project hygiene
- [ ] Delete stale docs: `README.md`, `QUICKSTART.md`, `WEB_INTERFACE.md`, `SUMMARY.md`, `API_EXAMPLES.md`, `VERCEL_DEPLOYMENT.md`
- [ ] Delete dead scripts: `start.sh`, `run_server.sh`, `test_api.py`, `requirements.txt` (or replace with real one)
- [ ] Write fresh `README.md` reflecting actual Vercel + serverless + Gemini stack
- [ ] Verify `vercel.json` `framework: fastapi` field — remove if it serves no purpose

### 0.2 Static asset extraction
- [ ] Create `static/` directory
- [ ] Extract HTML from `api/index.py` → `static/index.html`
- [ ] Extract CSS from inline `<style>` → `static/app.css`
- [ ] Extract JS from inline `<script>` → `static/app.js`
- [ ] Update `vercel.json` to serve `static/*` directly
- [ ] Reduce `api/index.py` to a 30-line redirect or static file serve
- [ ] Smoke test: `vercel dev`, confirm page renders identically

### 0.3 Gemini 2.0 enablement
- [ ] Confirm `gemini-2.0-flash` is available with the existing `GEMINI_API_KEY`
- [ ] Smoke-test grounded search via curl: `tools: [{google_search: {}}]`, query "Forest Essentials gift set under ₹2000 in India"
- [ ] Confirm response includes `groundingMetadata` with citation URLs
- [ ] Confirm region/availability for our Vercel deployment region
- [ ] Add `GEMINI_MODEL=gemini-2.0-flash` to Vercel env
- [ ] (Optional, only if Gemini grounding is weak) Sign up for Brave Search API free tier and store `BRAVE_SEARCH_KEY`

### 0.4 Affiliate program setup (start now — 24-48h approval cycles)
- [ ] Apply for Cuelinks (`cuelinks.com`) — pick "Indian shopping aggregator" category; covers Flipkart/Myntra/Croma/Ajio/ShoppersStop/Meesho in one signup
- [ ] Apply for Amazon Associates India (`affiliate-program.amazon.in`) — needs gifting-idea.vercel.app as the host site
- [ ] Once approved, add `AMAZON_AFFILIATE_TAG` (format: `yourname-21`) to Vercel env
- [ ] Once approved, add `CUELINKS_CID` to Vercel env
- [ ] Smoke-test by inspecting one product card's `BUY ON AMAZON` link in DevTools — confirm `?tag=...` is present
- [ ] Smoke-test by inspecting one Flipkart link — confirm it goes through `linksredirect.com`
- [ ] Add affiliate disclosure to footer: *"Some links earn us a small commission..."* (already in DESIGN.md voice)
- [ ] Note: code support is already shipped (`add_affiliate_tags()` in `api/recommend.py`); only needs env vars to activate

### 0.4 Tooling
- [ ] Create `.agents/skills/impeccable/scripts/` and seed if running impeccable commands locally (optional)
- [ ] Add a tiny `tools/devtest.py` for hitting `/api/recommend` from CLI without UI

---

## Phase 1 — Marketplace search (Weeks 2-3)

### 1.1 Cache layer
- [ ] `api/cache.py` — in-memory dict with TTL
- [ ] Helper: `get_or_set(key, ttl_hours, factory_fn)`
- [ ] Two cache buckets: `IDEAS_CACHE` (7d TTL, keyed by relationship+occasion+vibe+budget-bucket+gender) and `GROUNDED_CACHE` (24h TTL, keyed by gift idea title)
- [ ] Cache size cap (e.g. 500 entries each, LRU eviction)

### 1.2 Gemini grounded search client
- [ ] `api/search.py` — `ground_product(idea_title: str, budget_min: int, budget_max: int) -> Product | None`
- [ ] Calls Gemini 2.0 Flash with `tools: [{google_search: {}}]`
- [ ] Use `urllib.request` (stdlib, no new deps)
- [ ] Prompt instructs model to return strict JSON: `{title, price_inr, merchant, product_url, image_url}` plus emit grounding citations
- [ ] Parse response: prefer JSON block; fall back to `groundingMetadata` URLs if JSON missing
- [ ] Timeout: 15s per call; on failure return `None` (signals fallback)
- [ ] Cache hits via `cache.py`

### 1.3 URL validator
- [ ] `api/validators.py` — `is_product_url(url: str) -> bool`
- [ ] Regex per marketplace (Amazon `/dp/`, Flipkart `/p/`, Myntra `/buy`, Croma `/p/`)
- [ ] Optional `verify_url(url: str) -> bool` — HEAD with 2s timeout; if it fails, log and skip but don't block
- [ ] Reject obvious search/category URLs

### 1.4 Brave Search fallback (only if Gemini grounding is too weak)
- [ ] `api/search_brave.py` — only build if Phase 0.3 testing showed Gemini grounding is unreliable
- [ ] Same `Product` interface
- [ ] Used as backup when Gemini grounding returns no valid product URL

### 1.5 Prompt templates
- [ ] `api/prompts.py` — `build_ideas_prompt(...)` for LLM-1 (10 specific gift ideas, no grounding)
- [ ] `api/prompts.py` — `build_grounded_search_prompt(idea_title, budget, region)` for LLM-2 (one idea → one verified product)
- [ ] `api/prompts.py` — `build_personalization_prompt(verified_products, recipient_context)` for LLM-3 (personal "why this" copy)
- [ ] Move existing prompt strings out of `recommend.py` into `prompts.py`
- [ ] Each prompt function: pure, type-annotated, returns `str`

### 1.6 Orchestration update
- [ ] Refactor `api/recommend.py::get_recommendations` into a clear pipeline:
  1. `ideas = llm_generate_ideas(...)` (LLM-1, cached 7d)
  2. `verified = [ground_product(idea) for idea in ideas]` (LLM-2 grounded, cached 24h, parallel where possible)
  3. `valid = [v for v in verified if is_product_url(v.url) and in_budget(v.price)]`
  4. If `len(valid) < 6`: re-run grounding with looser budget for missing ideas
  5. `personalized = llm_personalize(valid, ...)` (LLM-3)
  6. `return assemble_response(personalized)`
- [ ] Each step has a fallback: if grounding fails entirely, run old rule-based recommender with search-page links
- [ ] Surface `data_source` in response: `"grounded"` / `"mixed"` / `"rule_based"`

### 1.7 Quick-commerce labels
- [ ] Add `quick_commerce_search_links` to each card: deep-link to Zepto/Blinkit/Instamart search
- [ ] Mark these clearly as "Search on [store]" not "Buy on [store]"

### 1.8 Feature flag rollout
- [ ] Cookie-based 50/50 split: `gg_v2_search=on|off`
- [ ] Old flow stays available behind the flag
- [ ] Log `data_source` and grounded-call latency to Vercel logs for monitoring

---

## Phase 2 — UI overhaul (Weeks 3-4)

### 2.1 Design tokens
- [ ] `static/app.css` :root section with OKLCH custom properties (per PRD §5.3)
- [ ] Type scale custom properties (per PRD §5.4)
- [ ] Spacing scale (4-8-12-16-24-32-48-64-96)
- [ ] Motion timing custom properties

### 2.2 Wizard
- [ ] State machine in `static/app.js`: `STEP_1` → `STEP_2` → ... → `RESULTS`
- [ ] Render function per step; only one step in DOM at a time
- [ ] Step 1: relationship grid
- [ ] Step 2: occasion grid
- [ ] Step 3: about-them chip groups
- [ ] Step 4: budget slider with live preview chip
- [ ] Step 5: optional notes textarea + skip
- [ ] URL hash sync (`#step-2`) for back-button support
- [ ] Pre-fill from sessionStorage on reload

### 2.3 Results screen
- [ ] Skeleton loader (10 placeholder cards) while API in flight
- [ ] Phased progress label: "Generating ideas → Searching stores → Personalizing"
- [ ] Card component (template-literal render, no framework)
- [ ] Sticky header with budget pill + share + brand
- [ ] Sticky footer with refine button
- [ ] Native `navigator.share()` integration with fallback to copy-link
- [ ] localStorage favorites (heart icon)

### 2.4 Responsive layout
- [ ] Mobile: single column, sticky bars
- [ ] Tablet (≥768px): 2-col card grid
- [ ] Desktop (≥1024px): 3-col card grid + wider wizard

### 2.5 Accessibility
- [ ] Every interactive element ≥44x44px tap target
- [ ] Wizard steps as `<form>` for native keyboard handling
- [ ] `aria-live="polite"` on results region
- [ ] Visible focus rings (saffron-coral 2px outline + offset)
- [ ] `prefers-reduced-motion` respected

---

## Phase 3 — Polish (Week 5)

### 3.1 Motion
- [ ] Card stagger entry on results render
- [ ] Wizard step slide+fade transitions
- [ ] Slider tick scale feedback
- [ ] Audit: nothing animating layout properties

### 3.2 States
- [ ] Empty state: SerpAPI returned 0 results in budget — friendly retry with budget bump
- [ ] Error state: API down — friendly fallback, show rule-based 5-card grid
- [ ] Loading state: pulse skeleton, never spinner-only

### 3.3 Quality passes
- [ ] Run `$impeccable audit` — fix all CRITICAL + HIGH
- [ ] Run `$impeccable critique` — UX heuristics review
- [ ] Lighthouse mobile audit; target ≥90
- [ ] Real-device test: iPhone 13 Safari, Pixel 7 Chrome, Galaxy A-series Chrome
- [ ] Bandit security scan on `api/`
- [ ] Manual: turn off SerpAPI key, confirm fallback path works

### 3.4 SEO + share
- [ ] Open Graph tags + 1200x630 share image at `assets/og-image.png`
- [ ] Twitter Card meta
- [ ] Favicon set (16, 32, 180-apple-touch)
- [ ] Sitemap.xml + robots.txt

---

## Phase 4 — Ship + iterate

### 4.1 Launch
- [ ] Merge feature flag at 50/50 → 100% over 3 days, watching dashboards
- [ ] Remove old code paths once 100% on v2 for 7 days
- [ ] Update Vercel project notes
- [ ] Tag release: `git tag v2.0.0`

### 4.2 Monitoring
- [ ] Enable Vercel Analytics
- [ ] Track Gemini daily request count vs free-tier 1,500 cap; alert at 80%
- [ ] Set up Sentry (free tier) for client + server errors
- [ ] Custom event tracking: wizard_step_complete, result_card_view, buy_cta_click, refine_click
- [ ] Track `data_source` distribution (grounded / mixed / rule_based) — leading indicator of grounding quality

### 4.3 First-week dashboards
- [ ] Outbound click-through rate
- [ ] Wizard completion funnel
- [ ] p95 latency
- [ ] SerpAPI cache hit rate
- [ ] LLM cost per session

### 4.4 Backlog (V3 candidates)
- Amazon Associates application + PA-API integration
- Curated quick-commerce SKU catalog
- Hindi locale
- Saved gift lists with shareable URL (Vercel KV)
- "Surprise me" mode (skip wizard, infer from minimal input)
- Gift reminders (calendar integration)

---

## Pre-flight checklist (before starting Phase 1)

- [ ] PRD reviewed and signed off
- [ ] Gemini 2.0 grounding smoke-tested and confirmed working (Phase 0.3)
- [ ] Static asset extraction complete (Phase 0.2)
- [ ] Stale docs cleaned (Phase 0.1)
- [ ] Branch strategy: `main` stays prod; work on `v2/phase-1`, `v2/phase-2` etc; merge via PR

## Definition of done (per phase)

A phase is done when:
1. All tasks above ticked
2. Code reviewed (use `code-reviewer` agent)
3. Smoke-tested on Vercel preview deployment
4. No new CRITICAL or HIGH issues from `$impeccable audit`
5. Brief written summary in PR description: what changed, what to verify, known gaps
