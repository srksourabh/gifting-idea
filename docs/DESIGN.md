# GiftingGenie — Design System

**Status:** v2 spec, paired with `PRD.md` and `PLAN.md`.
**Audience:** the developer (you, future-you, or Claude).
**Aesthetic in one line:** *brutalist scaffolding, gifting warmth — concrete and ink with marigold detonations.*

---

## 1. The design idea

HEAVYWEIGHT does menswear via brutalism: massive Anton type, concrete + ink, industrial cold, grayscale until you commit. GiftingGenie steals the **scaffolding** — asymmetry, mix-blend-difference, grain, mono utility text — and then **subverts** it at exactly the moments where gifting is supposed to feel warm: the submit CTA, the result reveal, the heart-save, the "delivered" badge.

The tension between *cold structural concrete* and *one warm marigold detonation* is the entire personality. GenZ reads this as confident, anti-corporate, ironic-but-sincere. It does not look like every other Indian e-commerce site (those reach for marigold + maroon + kalash emoji within 5 seconds — see anti-patterns).

**Reference vibes (for the developer's mental model):** Pangaia product pages, Cactus Plant Flea Market drops, Aimé Leon Dore lookbooks, Jacquemus invitations, MSCHF storefronts. **Not:** Nykaa, Igp.com, FNP, BlissfulGifts, anything with a kalash emoji.

---

## 2. Tokens

All tokens live in `static/app.css` `:root`. Use the CSS custom properties everywhere. Never hand-code raw hex inside a component.

### 2.1 Color

OKLCH only. Never `#000` or `#fff`. Every neutral is tinted toward a warm hue at chroma 0.003-0.008 — the warmth is invisible in isolation but it's what stops the page feeling clinical.

```css
:root {
  /* Surfaces */
  --concrete: oklch(0.945 0.003 80);   /* page background, the dominant surface */
  --paper:    oklch(0.985 0.005 80);   /* card surface, slightly brighter than concrete */
  --ink:      oklch(0.13  0.008 60);   /* primary text, near-black with hint of warmth */
  --ink-soft: oklch(0.30  0.008 60);   /* secondary text */
  --hairline: oklch(0.86  0.006 70);   /* 1px borders, dividers */

  /* The joy detonation — used SPARINGLY. See §3 for rules. */
  --marigold:        oklch(0.78 0.17 78);   /* the accent — saffron-yellow */
  --marigold-press:  oklch(0.70 0.19 72);   /* pressed/active state */
  --marigold-deep:   oklch(0.60 0.20 60);   /* on hover for high-emphasis surfaces */

  /* Functional / status */
  --live:    oklch(0.60 0.23 25);     /* coral-red — "live", scarcity, errors */
  --good:    oklch(0.62 0.16 155);    /* pistachio — success, delivered */
  --info:    oklch(0.55 0.10 240);    /* steel — neutral info, never primary */

  /* Inverted (for dark sections like footer) */
  --void:        oklch(0.10 0.005 60);  /* footer / dark sections */
  --void-text:   oklch(0.95 0.005 60);  /* text on void */
  --void-subtle: oklch(0.30 0.008 60);  /* dividers on void */
}

@media (prefers-color-scheme: dark) {
  :root {
    --concrete: oklch(0.16 0.005 60);
    --paper:    oklch(0.20 0.005 60);
    --ink:      oklch(0.95 0.005 60);
    --ink-soft: oklch(0.70 0.005 60);
    --hairline: oklch(0.30 0.006 60);
    /* marigold/live/good/info hold their values — they're tuned for both modes */
  }
}
```

**Color contract:**

| Role | Token | Usage cap |
|---|---|---|
| Background | `--concrete` | ~70% of surface |
| Text | `--ink` / `--ink-soft` | All text on concrete |
| Card | `--paper` | All elevated surfaces |
| Divider | `--hairline` | 1px only |
| **Accent** | `--marigold` | **≤ 8% of surface area, ever** |
| Status | `--live` / `--good` | Badges, dots, error text only |

### 2.2 Typography

Two-font system. Both load from Google Fonts.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@400;500;700&family=Khand:wght@500;600;700&display=swap" rel="stylesheet">
```

- **Anton** — display headlines, 400 only (it has one weight). Always uppercase. Always tight tracking, tight leading. The concrete-block voice.
- **Space Grotesk** — body, UI, utility. Variable weight 400-700. Slightly mechanical, GenZ-coded, reads cleanly at 12px for monospace-style metadata.
- **Khand** — Devanagari fallback for Anton. Same heavy-condensed energy, has native Hindi support. Use only when displaying Hindi (V3 territory).

```css
:root {
  --font-display: "Anton", "Khand", "Arial Narrow", sans-serif;
  --font-text:    "Space Grotesk", system-ui, -apple-system, sans-serif;

  /* Type scale — mobile baseline. All sizes in rem (1rem = 16px). */
  --t-mega:    6rem;     /* 96px — hero only, one per page */
  --t-display: 4rem;     /* 64px — section opens */
  --t-h1:      2.5rem;   /* 40px */
  --t-h2:      1.75rem;  /* 28px */
  --t-h3:      1.25rem;  /* 20px */
  --t-body:    1rem;     /* 16px */
  --t-small:   0.875rem; /* 14px */
  --t-mono:    0.75rem;  /* 12px — uppercase utility */

  /* Line heights, tightening as size grows */
  --lh-mega:    0.85;
  --lh-display: 0.9;
  --lh-h1:      0.95;
  --lh-h2:      1.05;
  --lh-h3:      1.2;
  --lh-body:    1.55;

  /* Tracking */
  --tr-display: -0.02em;
  --tr-body:    0;
  --tr-mono:    0.12em;
}

@media (min-width: 768px) {
  :root {
    --t-mega:    9rem;     /* 144px on tablet+ */
    --t-display: 6rem;     /* 96px */
    --t-h1:      3.5rem;   /* 56px */
  }
}

@media (min-width: 1280px) {
  :root {
    --t-mega:    12rem;    /* 192px on desktop — full HEAVYWEIGHT energy */
  }
}

/* Type role classes — use these instead of inline sizes */
.t-mega    { font-family: var(--font-display); font-size: var(--t-mega);    line-height: var(--lh-mega);    letter-spacing: var(--tr-display); text-transform: uppercase; }
.t-display { font-family: var(--font-display); font-size: var(--t-display); line-height: var(--lh-display); letter-spacing: var(--tr-display); text-transform: uppercase; }
.t-h1      { font-family: var(--font-display); font-size: var(--t-h1);      line-height: var(--lh-h1);      letter-spacing: var(--tr-display); text-transform: uppercase; }
.t-h2      { font-family: var(--font-display); font-size: var(--t-h2);      line-height: var(--lh-h2);      letter-spacing: var(--tr-display); text-transform: uppercase; }
.t-h3      { font-family: var(--font-text);    font-size: var(--t-h3);      line-height: var(--lh-h3);      font-weight: 700; letter-spacing: -0.01em; }
.t-body    { font-family: var(--font-text);    font-size: var(--t-body);    line-height: var(--lh-body);    font-weight: 400; }
.t-mono    { font-family: var(--font-text);    font-size: var(--t-mono);    line-height: 1.4;               font-weight: 500; letter-spacing: var(--tr-mono); text-transform: uppercase; font-variant-numeric: tabular-nums; }
```

**Body line length:** max 65ch. Enforce with `max-width: 65ch` on text containers.

### 2.3 Spacing

4px scale. Never use values outside this scale.

```css
:root {
  --s-1:   4px;
  --s-2:   8px;
  --s-3:   12px;
  --s-4:   16px;
  --s-5:   24px;
  --s-6:   32px;
  --s-7:   48px;
  --s-8:   64px;
  --s-9:   96px;
  --s-10:  128px;
  --s-11:  192px;  /* hero gutters on desktop */
}
```

**Asymmetry rule:** don't pad sections symmetrically. `padding: var(--s-9) var(--s-4) var(--s-7) var(--s-7)` is more brutalist than `padding: var(--s-7)`. See §4.2 hero.

### 2.4 Motion

```css
:root {
  --dur-instant: 80ms;    /* press feedback, tick scale */
  --dur-quick:   180ms;   /* hover state, link hover */
  --dur-base:    300ms;   /* most transitions */
  --dur-slow:    700ms;   /* signature: grayscale → color image reveal */
  --dur-glacial: 1200ms;  /* hero text entry, page intros */

  --ease-out:        cubic-bezier(0.22, 1, 0.36, 1);   /* ease-out-quart — default */
  --ease-out-expo:   cubic-bezier(0.19, 1, 0.22, 1);   /* sharper end */
  --ease-in-out:     cubic-bezier(0.65, 0, 0.35, 1);   /* state changes */
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Animate transform + opacity only.** Never animate width, height, top, left, padding, margin.

### 2.5 Effects

```css
:root {
  /* Sharp shadows — brutalism, not material */
  --shadow-press: 0 0 0 2px var(--ink);                    /* press = hard outline */
  --shadow-float: 4px 4px 0 0 var(--ink);                  /* offset hard shadow */
  --shadow-deep:  8px 8px 0 0 var(--ink);                  /* hover state on shadow-float */

  /* Z-index scale */
  --z-base:      0;
  --z-raised:    10;
  --z-sticky:    20;
  --z-overlay:   30;
  --z-modal:     40;
  --z-toast:     50;
  --z-cursor:    60;
}
```

**Border radius:** mostly 0. Brutalism is rectangular. Exceptions: the floating cart button (full circle) and the heart-save (full circle). Cards, inputs, buttons: `border-radius: 0`.

### 2.6 Grain overlay

The signature texture. Apply once on `<body>::before`.

```css
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: var(--z-cursor);
  opacity: 0.035;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  mix-blend-mode: multiply;
}
```

3.5% opacity, not 4% — we're a hair lighter than HEAVYWEIGHT because our base concrete is slightly warmer.

---

## 3. The marigold rule (read this twice)

Marigold is **not** a brand color you sprinkle. It's a punctuation mark. There are exactly five places it appears:

1. **The submit CTA** in the wizard's last step ("Find their gift")
2. **The Buy CTA** on a product card (background)
3. **The "live" status dot** when a result was generated less than 60s ago
4. **The hover state** on a saved-heart icon
5. **The grayscale-to-color image transition** on product cards (the image goes from gray to full saturation, NOT to marigold-tinted — but the transition itself feels like a marigold moment)

**Anywhere else, default to ink-on-concrete.** If you find yourself adding marigold to make something "pop," delete it. The whole reason it works is scarcity. Saturating with marigold turns this into an Igp.com clone within one PR.

---

## 4. Components

### 4.1 Non-standard header

Fixed top, full width. Logo wordmark top-left. Nav pushed right with extra margin to leave the hero space breathing. `mix-blend-difference` so it inverts against whatever scrolls under it.

```html
<header class="site-header">
  <a href="/" class="brand">
    <span class="t-h2 brand-mark">GIFTING<br>GENIE</span>
    <span class="t-mono brand-sub">EST. 2024 / IND</span>
  </a>
  <nav class="site-nav">
    <a href="#how" class="nav-link">HOW IT WORKS</a>
    <a href="#about" class="nav-link">ABOUT</a>
    <a href="#archive" class="nav-link">ARCHIVE</a>
  </nav>
</header>
```

```css
.site-header {
  position: fixed;
  inset: 0 0 auto 0;
  z-index: var(--z-sticky);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--s-5) var(--s-5);
  mix-blend-mode: difference;
  color: var(--concrete);  /* difference inverts this against whatever is behind */
  pointer-events: none;
}
.site-header > * { pointer-events: auto; }

.brand-mark { letter-spacing: -0.04em; line-height: 0.85; }
.brand-sub  { display: block; margin-top: var(--s-1); opacity: 0.7; }

.site-nav {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--s-2);
  margin-right: var(--s-7);  /* the "shifted right to avoid overlap" rule */
}

.nav-link {
  font-family: var(--font-text);
  font-size: var(--t-mono);
  letter-spacing: var(--tr-mono);
  text-transform: uppercase;
  text-decoration: none;
  color: inherit;
  transition: text-decoration var(--dur-quick) var(--ease-out);
}
.nav-link:hover { text-decoration: line-through; text-decoration-thickness: 2px; }

@media (max-width: 767px) {
  .site-nav { display: none; }
  .site-header { padding: var(--s-4); }
}
```

### 4.2 Asymmetric hero

Split, intentionally unbalanced. Left 42% holds a massive headline pushed *low* (so the header doesn't crash into it). Right 65% holds an oversized image with a partial off-screen crop. Yes, 42 + 65 = 107. It overlaps. That's the point.

```html
<section class="hero">
  <div class="hero-text">
    <h1 class="t-mega hero-headline">
      FIND<br>
      THEIR<br>
      GIFT.
    </h1>
    <p class="t-body hero-sub">
      Tell us five things. We pull real products from real shops, ranked for the person — not the algorithm.
    </p>
    <a href="#start" class="hero-cta t-mono">Start &rarr;</a>
  </div>

  <figure class="hero-image">
    <img src="/assets/hero.jpg" alt="A wrapped parcel against concrete">
    <span class="t-mono hero-collection">COLLECTION 004 · MAY 2026</span>
  </figure>
</section>
```

```css
.hero {
  position: relative;
  min-height: 100vh;
  min-height: 100dvh;
  padding: var(--s-11) var(--s-5) var(--s-7);
  overflow: hidden;
}

.hero-text {
  position: relative;
  z-index: var(--z-raised);
  width: 42%;
  margin-top: 30vh;  /* push low — clears the header, makes room for breath */
}

.hero-headline {
  margin-bottom: var(--s-5);
}

.hero-sub {
  max-width: 320px;
  margin-bottom: var(--s-5);
  color: var(--ink-soft);
}

.hero-cta {
  display: inline-block;
  border-bottom: 2px solid var(--ink);
  padding-bottom: 2px;
  text-decoration: none;
  color: var(--ink);
  transition: color var(--dur-quick) var(--ease-out), border-color var(--dur-quick) var(--ease-out);
}
.hero-cta:hover { color: var(--marigold-deep); border-color: var(--marigold-deep); }

.hero-image {
  position: absolute;
  right: -10%;          /* partial off-screen crop */
  top: 15%;
  width: 65%;
  height: 75%;
  margin: 0;
  filter: grayscale(1);
  transition: filter var(--dur-slow) var(--ease-out);
}
.hero-image img {
  width: 100%; height: 100%;
  object-fit: cover;
  object-position: left center;
}
.hero:hover .hero-image { filter: grayscale(0); }

.hero-collection {
  position: absolute;
  bottom: var(--s-4);
  left: var(--s-3);
  transform: rotate(-90deg);
  transform-origin: 0 0;
  color: var(--concrete);
  mix-blend-mode: difference;
}

@media (max-width: 767px) {
  .hero { padding: var(--s-9) var(--s-4) var(--s-5); }
  .hero-text { width: 100%; margin-top: 20vh; }
  .hero-image { width: 90%; right: -15%; top: auto; bottom: 5%; height: 35vh; }
}
```

### 4.3 Wizard step

One question per screen. The wizard is the heart of the app — every step is its own composition, not a generic form layout.

**Anatomy:**
- Step counter top-left in mono (`STEP 03 / 05`)
- Massive question in display type
- Decision area below: pill grid, chip group, slider, or textarea
- Persistent footer: "BACK" left mono, "SKIP" or counter middle, "NEXT →" right (only marigold on last step's submit)

```html
<section class="wizard-step" data-step="1">
  <div class="wizard-meta">
    <span class="t-mono">STEP 01 / 05</span>
    <button class="wizard-back t-mono" type="button">← BACK</button>
  </div>

  <h2 class="t-display wizard-question">
    Who's it<br>for?
  </h2>

  <div class="pill-grid">
    <button class="pill" data-value="mother">MOTHER</button>
    <button class="pill" data-value="father">FATHER</button>
    <!-- ... -->
    <button class="pill" data-value="saali">SAALI</button>
  </div>

  <footer class="wizard-foot">
    <span class="t-mono wizard-hint">TAP TO CONTINUE</span>
  </footer>
</section>
```

```css
.wizard-step {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;
  padding: var(--s-9) var(--s-5) var(--s-5);
  gap: var(--s-7);
}

.wizard-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--ink-soft);
}
.wizard-back {
  background: none;
  border: 0;
  color: inherit;
  cursor: pointer;
  font: inherit;
  padding: var(--s-2);
  margin: calc(-1 * var(--s-2));  /* expand hit area without visual change */
}

.wizard-question {
  align-self: end;
  margin: 0;
  letter-spacing: -0.04em;
}

/* Pill grid — relationship/occasion pickers */
.pill-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--s-1);
  margin-top: var(--s-5);
}
@media (min-width: 768px) {
  .pill-grid { grid-template-columns: repeat(3, 1fr); }
}

.pill {
  border: 1px solid var(--ink);
  background: transparent;
  padding: var(--s-5) var(--s-3);
  font-family: var(--font-display);
  font-size: var(--t-h3);
  letter-spacing: var(--tr-display);
  text-transform: uppercase;
  color: var(--ink);
  cursor: pointer;
  min-height: 72px;          /* touch target */
  text-align: left;
  transition: background var(--dur-quick) var(--ease-out), color var(--dur-quick) var(--ease-out), transform var(--dur-instant) var(--ease-out);
}
.pill:hover  { background: var(--ink); color: var(--concrete); }
.pill:active { transform: scale(0.97); }
.pill[aria-pressed="true"] { background: var(--ink); color: var(--concrete); }

/* Slider — budget step */
.budget-slider { /* see §4.7 */ }
```

**Wizard transitions:** when advancing, the current step slides left + fades to 0; the next step slides in from the right. 300ms each, ease-out-expo.

### 4.4 Product card

The card is where brutalism MEETS gifting joy. Plain white paper, ink text, mono utility — but the image is grayscale-to-color on hover, and the Buy CTA is the marigold detonation.

```html
<article class="product-card">
  <a href="..." class="product-link" target="_blank" rel="noopener">
    <figure class="product-media">
      <img src="..." alt="..." loading="lazy">
      <span class="detail-badge t-mono">VERIFIED</span>
    </figure>

    <div class="product-meta">
      <span class="t-mono product-store">AMAZON.IN</span>
      <h3 class="t-h3 product-title">Forest Essentials Sandalwood Body Care Hamper</h3>
      <div class="product-price-row">
        <span class="t-h3 product-price">₹2,499</span>
        <s class="t-mono product-mrp">₹2,999</s>
      </div>
      <p class="t-body product-why">
        Your saali always smells like she's just stepped out of a spa — this set is exactly that vibe, and the gold-foil packaging carries Diwali energy.
      </p>
    </div>
  </a>

  <div class="product-actions">
    <button class="heart" aria-label="Save"><svg>...</svg></button>
    <span class="cta-buy t-mono">BUY ON AMAZON →</span>
  </div>
</article>
```

```css
.product-card {
  background: var(--paper);
  border: 1px solid var(--ink);
  display: flex;
  flex-direction: column;
  position: relative;
  /* No shadow by default. Brutalism. */
}

.product-link {
  display: block;
  color: inherit;
  text-decoration: none;
}

.product-media {
  position: relative;
  aspect-ratio: 4 / 5;
  overflow: hidden;
  margin: 0;
  background: var(--hairline);
}
.product-media img {
  width: 100%; height: 100%;
  object-fit: cover;
  filter: grayscale(1);
  transform: scale(1);
  transition:
    filter var(--dur-slow) var(--ease-out),
    transform var(--dur-slow) var(--ease-out);
}
.product-card:hover .product-media img { filter: grayscale(0); transform: scale(1.05); }

.product-meta {
  padding: var(--s-4);
  display: flex;
  flex-direction: column;
  gap: var(--s-2);
}
.product-store { color: var(--ink-soft); }
.product-title {
  margin: 0;
  /* clamp to 2 lines */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.product-price-row {
  display: flex;
  align-items: baseline;
  gap: var(--s-2);
}
.product-mrp { color: var(--ink-soft); text-decoration-thickness: 1.5px; }
.product-why {
  font-size: var(--t-small);
  color: var(--ink-soft);
  max-width: 60ch;
}

.product-actions {
  display: flex;
  border-top: 1px solid var(--ink);
}
.cta-buy {
  flex: 1;
  background: var(--marigold);     /* the detonation */
  color: var(--ink);
  padding: var(--s-4);
  text-align: center;
  border: 0;
  border-left: 1px solid var(--ink);
  cursor: pointer;
  transition: background var(--dur-quick) var(--ease-out);
}
.cta-buy:hover { background: var(--marigold-press); }

.heart {
  width: 56px; height: 56px;
  background: var(--paper);
  border: 0;
  color: var(--ink);
  cursor: pointer;
  transition: color var(--dur-quick) var(--ease-out), transform var(--dur-instant) var(--ease-out);
}
.heart:hover           { color: var(--marigold-deep); }
.heart[aria-pressed="true"] { color: var(--marigold); }
.heart:active          { transform: scale(0.9); }
```

### 4.5 Detail badge

Small, sharp-cornered overlay on product images. Communicates a single technical fact in mono.

```css
.detail-badge {
  position: absolute;
  top: var(--s-2);
  right: var(--s-2);
  background: var(--paper);
  color: var(--ink);
  padding: 4px 8px;
  font-size: var(--t-mono);
  letter-spacing: var(--tr-mono);
  text-transform: uppercase;
  font-weight: 700;
}

/* Variants — pick exactly one per card */
.detail-badge--live   { background: var(--live); color: var(--paper); }
.detail-badge--quick  { background: var(--ink);  color: var(--concrete); }  /* "10 MIN" Blinkit */
.detail-badge--gold   { background: var(--marigold); color: var(--ink); }   /* curator's pick */
```

### 4.6 Results grid

Asymmetric. Not 3-up-evenly. Vary col-spans, vary aspect ratios, drop occasional negative margins for that pasted-poster feel. Mobile collapses to single column (asymmetry on a 375px screen reads as broken, not editorial).

```css
.results-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--s-4);
  padding: var(--s-5) var(--s-4);
}

@media (min-width: 768px) {
  .results-grid {
    grid-template-columns: repeat(12, 1fr);
    gap: var(--s-5);
    padding: var(--s-7) var(--s-5);
  }
  .results-grid > .product-card:nth-child(6n+1) { grid-column: span 7; }
  .results-grid > .product-card:nth-child(6n+2) { grid-column: span 5; margin-top: var(--s-9); }
  .results-grid > .product-card:nth-child(6n+3) { grid-column: span 5; }
  .results-grid > .product-card:nth-child(6n+4) { grid-column: span 7; margin-top: var(--s-7); }
  .results-grid > .product-card:nth-child(6n+5) { grid-column: span 6; }
  .results-grid > .product-card:nth-child(6n+6) { grid-column: span 6; margin-top: var(--s-9); }
}
```

**Card entry stagger:** when results render, each card animates in 60ms after the previous, `translateY(40px)` → `translateY(0)`, opacity `0` → `1`, 400ms ease-out-expo. Use Web Animations API or staggered CSS animation-delay.

### 4.7 Budget slider (the only marigold-on-input element)

Native `<input type="range">` is unstyleable across browsers. We rebuild it.

```html
<div class="budget-slider">
  <output class="t-mega slider-value">₹2,500</output>
  <span class="t-mono slider-hint">TYPICAL: CHOCOLATES, ACCESSORIES, GADGETS</span>
  <input type="range" min="500" max="50000" step="500" value="2500" id="budget" aria-label="Budget in rupees">
  <div class="slider-ticks" aria-hidden="true">
    <span>500</span><span>2K</span><span>5K</span><span>10K</span><span>25K</span><span>50K+</span>
  </div>
</div>
```

```css
.budget-slider input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 4px;
  background: var(--ink);
  outline: none;
  margin: var(--s-5) 0 var(--s-2);
}
.budget-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 28px; height: 28px;
  background: var(--marigold);    /* the detonation, again */
  border: 2px solid var(--ink);
  border-radius: 50%;
  cursor: grab;
  transition: transform var(--dur-instant) var(--ease-out);
}
.budget-slider input[type="range"]:active::-webkit-slider-thumb { transform: scale(1.2); }
.budget-slider input[type="range"]::-moz-range-thumb { /* mirror webkit */ }

.slider-value { display: block; }
.slider-hint  { display: block; color: var(--ink-soft); margin-top: var(--s-1); }
.slider-ticks {
  display: flex; justify-content: space-between;
  font-family: var(--font-text);
  font-size: var(--t-mono);
  letter-spacing: var(--tr-mono);
  color: var(--ink-soft);
}
```

### 4.8 Floating action button (save list / share)

Top-right, always visible, ink-on-paper, sharp shadow. Notification dot in `--live` for unsaved changes.

```html
<button class="fab" aria-label="Saved gifts">
  <svg width="20" height="20"><!-- heart icon --></svg>
  <span class="fab-badge t-mono">3</span>
</button>
```

```css
.fab {
  position: fixed;
  top: var(--s-5);
  right: var(--s-5);
  z-index: var(--z-overlay);
  width: 64px; height: 64px;
  border-radius: 50%;
  background: var(--paper);
  color: var(--ink);
  border: 1px solid var(--ink);
  box-shadow: 4px 4px 0 0 var(--ink);
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: transform var(--dur-quick) var(--ease-out), box-shadow var(--dur-quick) var(--ease-out);
}
.fab:hover  { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 0 var(--ink); }
.fab:active { transform: translate(2px, 2px);   box-shadow: 0 0 0 0 var(--ink); }

.fab-badge {
  position: absolute;
  top: -6px; right: -6px;
  min-width: 22px; height: 22px;
  background: var(--live);
  color: var(--paper);
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 10px;
  padding: 0 6px;
}
```

### 4.9 Footer

The structural anchor. `--void` background, oversized "GIFTING / GENIE" wordmark at low opacity at the bottom — not a watermark, a building.

```html
<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <p class="t-mono footer-label">PRODUCT</p>
      <ul><li><a href="/how">HOW IT WORKS</a></li><li><a href="/about">ABOUT</a></li></ul>
    </div>
    <div>
      <p class="t-mono footer-label">SHOPS</p>
      <ul><li>AMAZON.IN</li><li>FLIPKART</li><li>MYNTRA</li><li>CROMA</li></ul>
    </div>
    <div>
      <p class="t-mono footer-label">CONTACT</p>
      <ul><li>HELLO@GIFTINGGENIE.IN</li></ul>
    </div>
    <div>
      <p class="t-mono footer-label">LEGAL</p>
      <ul><li><a href="/terms">TERMS</a></li><li><a href="/privacy">PRIVACY</a></li></ul>
    </div>
    <div>
      <p class="t-mono footer-label">EST.</p>
      <p class="t-mono">2024 / NEW DELHI</p>
    </div>
    <div>
      <p class="t-mono footer-label">ISSUE</p>
      <p class="t-mono">004 / MAY 2026</p>
    </div>
  </div>

  <div class="footer-anchor" aria-hidden="true">
    <span class="footer-mega">GIFTING<br>GENIE</span>
  </div>
</footer>
```

```css
.site-footer {
  background: var(--void);
  color: var(--void-text);
  padding: var(--s-9) var(--s-5) 0;
  position: relative;
  overflow: hidden;
}
.footer-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--s-5) var(--s-4);
}
@media (min-width: 768px) {
  .footer-grid { grid-template-columns: repeat(6, 1fr); }
}
.footer-label { color: var(--void-subtle); margin-bottom: var(--s-2); }
.footer-grid ul { list-style: none; padding: 0; margin: 0; display: grid; gap: var(--s-1); }
.footer-grid a  { color: var(--void-text); text-decoration: none; font: var(--t-mono)/1.4 var(--font-text); letter-spacing: var(--tr-mono); text-transform: uppercase; }
.footer-grid a:hover { text-decoration: line-through; }

.footer-anchor {
  margin-top: var(--s-7);
  position: relative;
  pointer-events: none;
}
.footer-mega {
  display: block;
  font-family: var(--font-display);
  font-size: 22vw;          /* gigantic — the "structural anchor" rule */
  line-height: 0.85;
  text-transform: uppercase;
  color: rgb(255 255 255 / 0.06);
  letter-spacing: -0.04em;
  white-space: nowrap;
}
```

---

## 5. Interaction patterns

### 5.1 Link hover

Every text link — nav, footer, inline — uses `hover:line-through` with `text-decoration-thickness: 2px`. Never color change on link hover. The strikethrough is the gesture.

### 5.2 Button press

All buttons scale to 0.97 on `:active` for 80ms. Pill buttons additionally invert (background ink, text concrete). The marigold Buy CTA shifts to `--marigold-press` and does NOT scale (it's the destination, not the pre-action).

### 5.3 Image reveal

Every product image and hero image starts grayscale. On card hover (or hero scroll-into-view), `filter: grayscale(0)` over 700ms ease-out, with a subtle `scale(1.05)` happening in parallel. This is the signature.

### 5.4 mix-blend-difference

Use only on:
- The fixed header (auto-inverts against scrolling content)
- The hero "COLLECTION 004" rotated label (inverts against the hero image)

Anywhere else it gets ugly fast. Don't apply to body text.

### 5.5 Wizard transitions

Slide + fade. Outgoing step: `translateX(0)` → `translateX(-30%)`, opacity 1 → 0, 280ms ease-out-quart. Incoming step: `translateX(30%)` → `translateX(0)`, opacity 0 → 1, 320ms ease-out-quart, starting at 80ms delay (so the outgoing step is mostly gone first). Total wizard step transition: ~400ms.

### 5.6 Reduced motion

Already handled in §2.4. Test by enabling "Reduce motion" in OS settings; everything should still work, just snappier.

---

## 6. Accessibility (non-negotiables)

These come from the impeccable laws + the WCAG/Apple HIG checks. None of these are skippable.

- **Contrast:** text vs background ≥ 4.5:1. The combinations `--ink` on `--concrete` (≈ 16.5:1) and `--ink` on `--marigold` (≈ 8.2:1) both pass. `--ink-soft` on `--concrete` is ≈ 7.3:1 — still passes.
- **Touch targets:** min 44 × 44 px. Pills are 72px. Heart is 56px. Nav links use generous padding for hit area.
- **Focus rings:** every interactive element gets a 2px solid `--ink` outline with 3px offset. Never `outline: none` without replacement.
- **Skip link:** first element in `<body>`, visually hidden until focused. `Skip to content`.
- **Heading order:** never skip levels. Hero is `h1`, results header is `h1` on the results page (not h2 — they're separate logical pages).
- **`prefers-reduced-motion`:** already wired. Don't add motion that ignores it.
- **`prefers-color-scheme`:** dark mode tokens already defined. Test both.
- **Forms:** every input has a visible label. Errors below the field, in `--live`, with `role="alert"`.
- **Alt text:** every product image gets `alt="[product title]"`. Decorative images (grain, hero) get `alt=""`.

```css
:focus-visible {
  outline: 2px solid var(--ink);
  outline-offset: 3px;
}
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  position: fixed;
  top: var(--s-2);
  left: var(--s-2);
  z-index: var(--z-toast);
  background: var(--ink);
  color: var(--concrete);
  padding: var(--s-3);
  text-decoration: none;
}
```

---

## 7. Anti-patterns (read this with caffeine)

These come from impeccable's absolute bans plus failures I expect this aesthetic to drift toward. If you catch yourself doing any of these, rewrite the element with different structure.

| Anti-pattern | Why it kills | Do this instead |
|---|---|---|
| Side-stripe colored borders on cards (`border-left: 4px solid orange`) | SaaS cliché. Every status component since 2015. | Full borders, background tints, leading numbers |
| Gradient text (`background-clip: text` + linear-gradient) | Decorative, never meaningful. AI slop tell. | Single solid color. Emphasis via weight or size |
| Glassmorphism navbars (`backdrop-filter: blur`) | Reads "designed in 2021." Mix-blend-difference replaces this entirely. | The mix-blend-difference header in §4.1 |
| Hero-metric template (giant number + label + supporting stats + gradient accent) | The single most overused SaaS layout. | The hero in §4.2 is structural, not metric-flexing |
| Identical card grids (3-up-evenly, same icon + heading + text per card) | Unbearable. | Asymmetric grid in §4.6 |
| Diwali-cliché reflex (orange + maroon + diya emoji + kalash) | What every Indian gifting site reaches for in 4 seconds. | Concrete + ink + ONE marigold detonation |
| Marigold everywhere ("for warmth") | Destroys the rule that makes it work. | §3 — five places only |
| Border radius on cards/buttons | Softens the brutalism. | `border-radius: 0` |
| Icon-only buttons without aria-label | Inaccessible. | Always label, even decorative icons get `aria-hidden="true"` |
| Animating padding/margin/width/height | Janky on mobile. | `transform` + `opacity` only |
| Drop shadows that try to look real (`0 4px 12px rgba(0,0,0,0.08)`) | Material Design tell. | Sharp offset shadow in §2.5 (`4px 4px 0 0 var(--ink)`) — or no shadow |
| Modal as first thought | Lazy. | Inline expand or progressive disclosure first; modal only when truly necessary |
| Em dashes in copy | Dated typography tic. | Comma, colon, semicolon, period, parens |
| Title case in display headlines | Reads soft. Brutalism is uppercase. | Always uppercase for `--font-display` |
| Hindi pasted into Anton | Anton has zero Devanagari. Falls back to Arial. | Khand for Hindi (configured in font stack) |

---

## 8. Implementation checklist

Ordered. Don't skip steps.

- [ ] Wire fonts (Anton + Space Grotesk + Khand) via `<link>` in `static/index.html`
- [ ] Drop §2.1-§2.5 tokens into `:root` of `static/app.css`
- [ ] Add grain overlay (§2.6)
- [ ] Build §4.1 header — verify mix-blend-difference inverts correctly when scrolling under a dark image
- [ ] Build §4.2 hero — confirm asymmetry holds at 768px and 1280px breakpoints
- [ ] Build §4.3 wizard step component once; reuse for all 5 steps
- [ ] Build §4.4 product card; verify grayscale-to-color on real images
- [ ] Build §4.6 results grid; verify asymmetric layout doesn't break with <6 cards (write a fallback)
- [ ] Build §4.7 budget slider with `--marigold` thumb
- [ ] Build §4.8 FAB
- [ ] Build §4.9 footer with the giant wordmark
- [ ] Run impeccable audit / Lighthouse a11y; fix anything below 90
- [ ] Test on real iPhone Safari + Pixel Chrome
- [ ] Test with OS-level "Reduce motion" enabled
- [ ] Test with OS-level "Dark mode" enabled
- [ ] Test at 200% browser zoom (text scaling) — nothing should clip

---

## 9. Voice & copy

The visual system above means nothing if the copy reads like a SaaS sales page. The copy register is:

- **Confident, clipped, present-tense.** "FIND THEIR GIFT." Not "Discover the perfect gift for your loved one."
- **GenZ-coded but not try-hard.** No "fr fr no cap." No emojis in body copy. The aesthetic is the irony; the words stay clean.
- **Specific, not generic.** "Forest Essentials sandalwood hamper" not "luxurious skincare gift." "Your saali's exact aesthetic" not "perfect for her."
- **Indian without being cliché.** Use Hinglish where natural ("saali's vibe," "Diwali energy"), but don't perform it.
- **Mono labels, body in regular weight.** All UI labels in Space Grotesk uppercase tracking-wide. All paragraph copy in Space Grotesk regular sentence case.

**Examples:**

| Before (SaaS-coded) | After (GiftingGenie voice) |
|---|---|
| "Discover thoughtful gifts for your loved ones" | "FIND THEIR GIFT." |
| "Tell us about the recipient" | "WHO'S IT FOR?" |
| "Set your budget" | "HOW MUCH ARE WE SPENDING?" |
| "Find Recommendations" | "GO →" |
| "Purchase on Amazon" | "BUY ON AMAZON →" |
| "Generated by AI" | "10 IDEAS, READ EACH" |
| "Sorry, no results found" | "NOTHING IN BUDGET. STRETCH IT?" |

---

*This document is the source of truth for v2 visual design. If a component isn't here, ask before inventing one — and if you invent one, add it back to this file in the same PR.*
