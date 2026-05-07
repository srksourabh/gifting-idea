# GiftingGenie v2 — Product Requirements Document

**Author:** Sourabh Bhaumik (with Claude)
**Status:** Draft for review
**Date:** 2026-05-06
**Target ship:** Phased over 4-5 weeks

---

## 1. Why this v2 exists

GiftingGenie today gets the *idea* right and the *purchase* wrong. The model suggests a smart gift, then hands the user a search-results URL and hopes they figure it out from there. On a phone, the page is also too dense to use one-handed.

Two problems, one PRD:

1. **The links don't actually solve "where do I buy this"** — they drop you at marketplace search pages, not real products with real prices. The user has to do the work the app promised to do.
2. **The UI is desktop-first.** Most Indian gift research happens on a phone, often last-minute, often standing in line at a billing counter. The current single-page form is dense, scroll-heavy, and visually flat.

v2 fixes both: real product cards with verified live links, and a mobile-first wizard that respects how people actually use this.

---

## 2. Goals

| Goal | Measurable outcome |
|---|---|
| Recommendations resolve to real, in-stock products | ≥80% of cards link to a live product page (not search) |
| Real prices match the user's budget | 100% of cards within 60-130% of stated budget |
| Mobile-first | Lighthouse mobile score ≥90; ≥70% of sessions start and complete on mobile |
| Outbound click-through | ≥40% of viewers click a Buy CTA |
| Wizard completion | ≥75% of users who start step 1 reach results |

## 3. Non-goals

- Native iOS/Android app
- User accounts, saved gifts, history beyond local storage
- In-app cart or checkout (we deep-link, we don't sell)
- Promising real-time stock for quick-commerce (Zepto/Blinkit catalogs aren't public)
- Replacing Gemini with a different LLM

---

## 4. Marketplace integration

### 4.1 Honest reality check

Before specifying the solution, the constraints:

| Source | Public API? | Verdict |
|---|---|---|
| Amazon India | PA-API exists, but requires Amazon Associates approval + 3 qualifying sales in 180 days | Phase 2 only |
| Flipkart | Affiliate API closed to new applicants since 2022 | Not viable |
| Myntra, Croma, Ajio | No public APIs | Not viable directly |
| Zepto, Blinkit, Instamart | No public APIs at all; products gated behind app auth | Not viable directly |
| Direct scraping | Brittle, ToS-violating, blocked by Cloudflare | Not viable on serverless |

**Free options for live product discovery (the recommended path):**

| Option | Free tier | Trade-offs |
|---|---|---|
| **Gemini 2.0 Flash + Google Search grounding** | Generous: 15 RPM, 1,500 requests/day, 1M tokens/min | URL quality varies; sometimes returns category pages instead of product pages |
| **Brave Search API** | 2,000 queries/month free | Shopping vertical limited; primarily web results |
| **Google Programmable Search Engine** | 100 queries/day free, then $5/1k | Requires custom CSE setup; not shopping-specific |

Paid options exist (SerpAPI ~$75/mo, Oxylabs scrapers, etc.) but we're staying free until traffic justifies the spend.

### 4.2 Recommended approach — fully free

**Phase 1 (V2 launch): Gemini 2.0 Flash with Google Search grounding.**

Gemini 2.0+ supports `tools: [{google_search: {}}]` natively. One API call:
- Generates contextual gift ideas
- Live-searches the web for those products on Indian marketplaces
- Returns response with cited URLs (Amazon, Flipkart, Myntra, etc.)
- Includes a `groundingMetadata` block with the actual sources

This is on Gemini's **free tier** — same `GEMINI_API_KEY` we already use, no new account, no subscription. The free tier is 15 requests/minute and 1,500 requests/day, which comfortably covers early traffic.

For quick-commerce (Zepto / Blinkit / Swiggy Instamart), we deep-link to their search page with the product name as the query. We label these clearly: *"Quick deliver — search Blinkit"* vs *"View on Amazon"* so the user knows what to expect.

**Phase 2 (when free quota becomes a constraint): Brave Search free tier as fallback / hybrid.**

Brave Search API gives 2,000 queries/month free. Use it when Gemini grounding returns weak URLs (category pages, dead links). Sign up only if needed.

**Phase 3 (post-launch, traffic-permitting): Apply for Amazon Associates.**

Once we have traffic, register for Amazon Associates India. PA-API gives cleaner Amazon data, lets us add affiliate tags to URLs (revenue), and lets us verify ASIN-level availability.

**Phase 4 (later): Curated quick-commerce catalog.**

For "I need this in 10 minutes" use cases, maintain a small curated SKU list with stable Zepto/Blinkit deep links. Surface as a separate "Need it today?" filter on results.

### 4.7 Affiliate revenue (every outbound link, where possible)

Every product link going out to a marketplace where we have an affiliate program **must** be wrapped with the affiliate tag. Cost: zero. Effort: tiny. Upside: real revenue without changing the product.

The system uses a single server-side function (`add_affiliate_tags(links)` in `api/recommend.py`) that runs on every URL before the response is sent to the browser. The function reads three env vars and applies whichever programs are configured:

| Env var | Program | Coverage | When to use |
|---|---|---|---|
| `AMAZON_AFFILIATE_TAG` | Amazon Associates India | Amazon.in only | **Always.** Easiest to get; once approved you keep tagging Amazon URLs forever. Format: `yourname-21` (the `-21` is the India locale). |
| `CUELINKS_CID` | Cuelinks (aggregator) | Flipkart, Myntra, Croma, Ajio, ShoppersStop, Meesho, 1500+ merchants | **Recommended.** One signup, covers everyone except Amazon and quick-commerce. Wraps URLs through `linksredirect.com`. |
| `EARNKARO_TOKEN` | EarnKaro (alt aggregator) | Similar coverage to Cuelinks | Optional — only if Cuelinks rejects you. India-specific. |

**Order of preference inside the wrapper:**
1. Amazon URLs → direct `?tag=...` append (preserves a recognizable amazon.in URL, no redirect)
2. Other supported merchants → wrap through Cuelinks if `CUELINKS_CID` is set
3. Quick commerce (Blinkit, Zepto, Instamart, Swiggy) → never wrapped (no affiliate program exists)
4. If no env vars are set → links pass through unchanged

**Already implemented as of 2026-05-06.** Currently active for both the AI-powered (LLM-1 + LLM-2) and rule-based fallback recommendation paths. Set the env vars in Vercel and revenue starts on the next deploy — no code changes required.

**Roadmap for affiliate work:**

| Phase | Action |
|---|---|
| Phase 0 | Apply for Cuelinks now ([cuelinks.com](https://www.cuelinks.com/)) — 24-48h approval typical. Set `CUELINKS_CID` in Vercel env. |
| Phase 0/1 | Apply for Amazon Associates ([affiliate-program.amazon.in](https://affiliate-program.amazon.in/)) — needs site (we have one), needs 3 qualifying sales in 180 days to maintain. Set `AMAZON_AFFILIATE_TAG`. |
| Phase 2 | When Amazon PA-API integration lands, the tag carries through automatically (PA-API URLs already include the affiliate tag baked in). |
| Phase 3 | Add an affiliate-disclosure footer string per Indian advertising guidelines: *"Some links may earn us a small commission. Recommendations are not influenced by this."* |

**Reporting:** Cuelinks dashboard tracks clicks + conversions per merchant. Amazon Associates has its own dashboard. Reconcile monthly. No revenue tracking inside our app for v2 — keep it simple.

**Disclosure copy** (lives in footer + once per results screen as small mono text):

> *Some links earn us a small commission when you buy. Recommendations are picked for fit, not commission rate.*

### 4.3 New recommendation flow

```
User submits form
  ↓
LLM-1 (Gemini 2.0 Flash, NO grounding): Generate 10 specific gift ideas
  • Not just "Smart Watch" — "Noise ColorFit Pro 4 smartwatch"
  • Each idea has: title, gift_type, est_price, why-this snippet
  ↓
LLM-2 (Gemini 2.0 Flash, WITH google_search grounding): For each idea,
  search the live web and return:
    • Real product URL (Amazon/Flipkart/Myntra/Croma)
    • Verified product title (corrected if needed)
    • Real current price in INR
    • Image URL from the citation
  • Process in batches of 3-5 to stay within token / rate limits
  ↓
Validate
  • Drop results where URL is just a search page or category page
  • Drop results outside 60-130% of budget
  • Drop results without an image URL
  • If <6 valid products survive, retry round-2 with looser bounds
  ↓
LLM-3 (lightweight): Write personal "why this for you" copy for each verified product
  • Uses verified title + recipient context + user's note
  ↓
Return: cards with image, real price, real merchant, real deep link, why-applicable
```

**Three Gemini calls instead of two**, but all on free tier. The grounded call is the new bit; the rest is similar to today.

### 4.4 URL validation

Real product URLs have predictable patterns:

| Marketplace | Product URL pattern | Search/category pattern (REJECT) |
|---|---|---|
| Amazon India | `amazon.in/.../dp/[ASIN]` or `amazon.in/dp/[ASIN]` | `amazon.in/s?k=...` |
| Flipkart | `flipkart.com/[slug]/p/[item-id]` | `flipkart.com/search?q=...` |
| Myntra | `myntra.com/[category]/[brand]/[slug]/[id]/buy` | `myntra.com/[query]` |
| Croma | `croma.com/[slug]/p/[id]` | `croma.com/searchB?q=...` |

A URL passes validation if it matches the product pattern for a known marketplace AND returns a 2xx on a HEAD request (best-effort, 2s timeout, skip on failure).

### 4.5 Caching

- **Grounded search results** cached by normalized query string for 24h
  - In-memory per serverless instance (free, partial hit rate across instances)
  - Optional: Vercel KV later for cross-instance cache
- **LLM-1 ideas** cached by hash of (relationship, occasion, vibe, budget bucket, gender) for 7 days
- **LLM-3 personalization** never cached (uses personal note, varies per user)

Target: stay well under free-tier rate limits via cache hits.

### 4.6 Failure modes

| Failure | Behavior |
|---|---|
| Gemini free quota exhausted (1,500/day) | Fall back to current "search-page link" flow with soft notice |
| Grounding returns mostly invalid URLs | Re-run grounding with stricter prompt; else fall back to search-page links |
| URL HEAD validation fails | Skip that product; backfill from next-best |
| <6 valid products after both rounds | Mix verified + search-page-link cards; mark search-link cards clearly |
| Gemini API down entirely | Use rule-based recommender (already exists) |

---

## 5. UX/UI overhaul

### 5.1 Design register

**Brand register.** This is a B2C consumer product where the design IS the experience. The feeling — anticipation, generosity, joy — has to come through the interface.

### 5.2 The scene sentence

> *A 28-year-old in Bengaluru, on a phone, in a Uber to a cousin's engagement, realizing they forgot to get something — using one thumb, with 12 minutes to figure it out.*

That sentence determines everything below. **Theme: light**, because it's daylight, in transit, mixed with notifications and other apps. **Layout: vertical, one-thumb reachable.** **Speed: every step <3 seconds of cognitive load.**

### 5.3 Color, type, motion, components

**Source of truth:** `docs/DESIGN.md`.

The visual system is HEAVYWEIGHT-inspired brutalism, GenZ-adapted: Anton + Space Grotesk type, concrete + ink palette with a single marigold detonation, asymmetric layouts, mix-blend-difference header, grayscale-to-color image reveals, sharp offset shadows. See `DESIGN.md` for full token tables, component specs, interaction patterns, and explicit anti-patterns.

The sections below describe layout/flow/UX. Anything visual (color, type, spacing, motion, component appearance) defers to `DESIGN.md`.

### 5.4 Typography

See `DESIGN.md §2.2`. Anton for display (uppercase, tight tracking), Space Grotesk for body and mono utility, Khand as Devanagari fallback.

### 5.5 The wizard — one decision per screen

Ditches the current single-page form. Each screen asks one thing, has one decision, advances on tap.

**Step 1 — "Who's it for?"**
- Two-column grid of pill cards
- Mom, Dad, Wife, Husband, Brother, Sister, Saali, Boss, Friend, Boyfriend, Girlfriend, Colleague, Cousin, Other
- Each card: emoji + relationship, ~80px tap height
- Tap to advance

**Step 2 — "What's the occasion?"**
- 3-column emoji grid
- Diwali, Birthday, Anniversary, Wedding, Raksha Bandhan, Karwa Chauth, Eid, Holi, House Warming, Promotion, Just Because, Other
- Tap to advance

**Step 3 — "Tell us about them"**
- Single screen, three chip groups stacked
- Age band: Kid / Teen / 20s / 30s / 40s / 50s+
- Gender (optional, "Skip" prominent): Male / Female / Other / Prefer not to say
- Their vibe: Traditional / Modern / Quirky / Luxe (multi-select up to 2)
- Continue button bottom

**Step 4 — "Budget"**
- Big slider (snap points: ₹500, ₹1k, ₹2k, ₹3.5k, ₹5k, ₹10k, ₹15k, ₹25k, ₹50k+)
- Live preview chip below: *"₹2,500 → typical: chocolates, accessories, gadgets"*
- Tick scales 1.2x for 80ms on each snap (visual feedback)

**Step 5 — "Anything special?" (optional)**
- Single textarea, 280-char limit, character counter
- Skip CTA same prominence as Submit
- *"Like… they're vegan, into anime, learning guitar — anything to make it personal."*

**Submit**
- Skeleton loader: 10 card placeholders shimmer
- Real progress: "Generating ideas → Searching across stores → Personalizing for you" (3 phases)
- Average 5-7s end-to-end

### 5.6 Results screen

**Sticky header (mobile):**
- Brand mark left
- Budget pill center: *"₹2,500"* (tap to edit)
- Share button right (native share sheet)

**Card design:**
- Product image, 16:9, full-width on mobile, lazy-loaded
- Store badge: small pill top-right of image (Amazon / Flipkart / Myntra / Croma)
- Title: 2 lines max, truncated with ellipsis
- Price row: actual price prominent, MRP strikethrough small if available
- Tag chips: gift type (Funky / Formal / Romantic / Practical / Traditional / Luxe) + delivery hint
- *Why this:* 2-line teaser, "Read more" expands inline
- Primary CTA: "Buy on [store]" — full-width button, saffron-coral
- Secondary: heart icon to save (localStorage)

**Layout:**
- Mobile: vertical stack with horizontal swipe between cards if user prefers
- Tablet: 2-col grid
- Desktop: 3-col grid

**Sticky footer (mobile):**
- "Refine" button reopens wizard with pre-filled values
- Position count: "3 of 10"

### 5.7 Forbidden patterns

See `DESIGN.md §7` for the full anti-pattern table. Highlights: no side-stripe borders, no gradient text, no glassmorphism, no Diwali cliché, no border radius on cards/buttons, no marigold outside the five sanctioned places.

### 5.8 Motion

- Card entry: stagger 60ms each, ease-out-expo, 400ms total
- Wizard transitions: 300ms slide + fade, ease-out-quart
- Slider tick: scale 1.2x for 80ms on snap
- All motion uses `transform` + `opacity` only — no layout-property animation
- Respect `prefers-reduced-motion`

---

## 6. Technical architecture

### 6.1 New file structure

```
api/
  index.py          → thin handler, serves static/index.html (currently 71KB; will shrink to ~2KB)
  recommend.py      → orchestrates LLM-1 → search → LLM-2
  search.py         → NEW: SerpAPI client + caching
  prompts.py        → NEW: Gemini prompt templates as functions
  cache.py          → NEW: in-memory cache helpers
  favicon.py        → unchanged

static/
  index.html        → extracted from api/index.py
  app.css           → design tokens + components
  app.js            → wizard state machine, results render (vanilla, no framework)

docs/
  PRD.md            → this doc
  PLAN.md           → execution plan with task breakdown
  DESIGN.md         → token system + component reference (auto-generated post-Phase-2)

assets/
  cover.png         → existing
  og-image.png      → NEW: 1200x630 share preview
```

### 6.2 New env vars

| Variable | Required | Default | Source |
|---|---|---|---|
| `GEMINI_API_KEY` | yes | — | existing |
| `GEMINI_MODEL` | no | `gemini-2.0-flash` | switch to 2.0+ to enable grounding |
| `BRAVE_SEARCH_KEY` | optional (Phase 2 fallback) | — | brave.com/search/api/ free tier |
| `AMAZON_AFFILIATE_TAG` | revenue | — | affiliate-program.amazon.in (e.g. `yourname-21`) |
| `CUELINKS_CID` | revenue | — | cuelinks.com (aggregator covering Flipkart/Myntra/Croma/Ajio/+) |
| `EARNKARO_TOKEN` | optional | — | earnkaro.com (alternative aggregator) |
| `CACHE_TTL_HOURS` | no | 24 | — |
| `BUDGET_MIN_PCT` | no | 60 | — |
| `BUDGET_MAX_PCT` | no | 130 | — |

### 6.3 Performance budget

| Metric | Target |
|---|---|
| TTFB | <1s |
| Hero render | <3s |
| Wizard step transition | <100ms |
| Recommendation API end-to-end (p95) | <8s |
| Mobile JS bundle | <50KB gzipped |
| Mobile CSS bundle | <20KB gzipped |
| Lighthouse mobile score | ≥90 |

### 6.4 No-framework decision

Stays vanilla JS. Reasons:
- Current bundle is zero-framework; introducing React adds 40KB+ minified for no real win
- Wizard state is small enough for a hand-rolled state machine
- Vercel function cold starts already eat the latency budget; don't add more
- Easier for a future maintainer to read

If wizard logic balloons past ~500 lines, revisit with HTMX or Alpine — not React.

---

## 7. Phased rollout

### Phase 0 — Foundation (Week 1)
- Extract HTML/CSS/JS out of `api/index.py` into `static/`
- Set up DESIGN.md token system (run `$impeccable document` after extraction)
- Sign up for SerpAPI, store key in Vercel env
- Delete stale docs (README, QUICKSTART, etc.) per CLAUDE.md cleanup list, replaced with new ones from this PRD

### Phase 1 — Marketplace search (Weeks 2-3)
- Build `api/search.py` with SerpAPI client
- Build `api/cache.py` for in-memory caching
- Update `api/prompts.py` with new LLM-1 prompt (search-query-generator)
- Update `api/prompts.py` with new LLM-2 prompt (verified-product personalizer)
- Wire orchestration in `api/recommend.py`
- Add fallback path when SerpAPI fails
- Deploy behind feature flag (50/50 traffic split via cookie)

### Phase 2 — UI overhaul (Weeks 3-4)
- Build wizard (5 steps, vanilla JS state machine)
- Build results screen with new card component
- Implement design tokens, typography, motion
- Native share sheet integration
- Local-storage favorites
- Replace old UI on staging branch first; soak 48h

### Phase 3 — Polish (Week 5)
- Animation pass
- Empty / error / loading states
- Accessibility audit (run `$impeccable audit`)
- Mobile device testing (real iOS Safari, Android Chrome)
- Lighthouse pass
- Open Graph image, share metadata

### Phase 4 — Ship + iterate
- Roll to 100%
- Add Vercel Analytics
- Watch dashboards for: SerpAPI cost, click-through rate, refine rate, completion rate

---

## 8. Success metrics

| Metric | Baseline | Target (30 days post-launch) |
|---|---|---|
| Outbound click-through | unknown, est <10% | ≥40% |
| Wizard completion (start → results) | n/a | ≥75% |
| p95 results latency | n/a | <8s |
| SerpAPI cache hit rate | 0% | ≥30% |
| 30-day return rate | unknown | ≥15% |
| Lighthouse mobile | unknown | ≥90 |
| Cost per session (LLM + SerpAPI) | $0 | ≤$0.04 |

## 9. Costs

Rough monthly at 5,000 sessions, fully free path:

| Item | Cost |
|---|---|
| Gemini 2.0 Flash (3 calls per session, free tier covers 1,500 req/day) | $0 |
| Brave Search free tier (only if needed, 2k/mo) | $0 |
| Vercel hosting | $0 (free tier) |
| **Total** | **$0/mo** |

**Scaling considerations:**
- Gemini free tier hard cap: 1,500 requests/day. With 3 calls per session that's ~500 sessions/day before hitting the cap. Caching extends this materially.
- If we exceed free quota: Gemini paid is $0.075 per 1M input tokens / $0.30 per 1M output (Flash 2.0) — still far cheaper than SerpAPI. Estimated $5-15/mo at 5k sessions.
- Affiliate revenue (Phase 3+) is upside, not a dependency.

## 10. Risks & mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Gemini free quota (1,500/day) exhausts | Medium | Aggressive 24h cache + ID-bucket cache + graceful fallback to current flow |
| Grounded search returns category pages, not product pages | High | URL pattern validation per marketplace + HEAD check; reject and retry |
| Grounded search hallucinates URLs that 404 | Medium | HEAD validation with 2s timeout; skip and backfill from next-best |
| Affiliate approval takes >6mo | High | Don't budget revenue from it for V2 |
| Quick-commerce search-deep-link rejected by users | Medium | Label clearly; track CTR separately; build curated catalog later |
| Mobile Safari/Chrome rendering quirks | Low | Real-device testing before launch |
| Wizard feels slower than current single page | Medium | Snappy transitions (<100ms); show staged progress |
| Gemini 2.0 grounding region availability | Low | Confirm available for India / our Vercel region during Phase 0 |

## 11. Open questions

1. **Affiliate disclosure** — Once we add affiliate tags (Phase 2), legal copy needed. Where does it live? Footer + per-card asterisk?
2. **Quick-commerce strategy** — V2 does search-page deep links. Acceptable to launch with this, or block until we curate?
3. **Save & share** — Local-storage only for V2, or do we want a "share this gift list" URL that backs to KV? Adds infra; defer to V3?
4. **Multi-language** — Hindi for Tier-2/3? Out of scope for V2; flag for V3.
5. **Image rights** — SerpAPI returns image URLs hosted by Google/merchants. Do we hot-link or proxy? Hot-link saves cost but is technically against some merchants' ToS. Recommendation: hot-link for V2, proxy if any C&D.

---

## 12. Decision log

| Decision | Rationale |
|---|---|
| Gemini 2.0 grounding over SerpAPI | Free tier; one fewer service to integrate; URL quality acceptable with validation |
| Three Gemini calls instead of two | Splits ideation from grounded search from personalization — better cache reuse and quality |
| URL pattern validation per marketplace | Catches the main grounded-search failure mode (category/search pages instead of product pages) |
| Vanilla JS over React | Bundle size discipline; current code has no framework; wizard is small |
| Gemini stays | Already wired; free tier covers V2 entirely; no reason to swap |
| Mobile-first wizard over single-form | Matches actual usage; reduces cognitive load per screen |
| Saffron-coral as carrying color | Warm and Indian without category-reflex Diwali clichés |
| No user accounts | Out of scope; localStorage covers favorites; KV adds infra burden |

---

*See `docs/PLAN.md` for the task-level execution plan.*
