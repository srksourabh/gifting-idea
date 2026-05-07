/* ==========================================================================
   GiftingGenie v3 — app.js
   Vanilla JS wizard state machine + results renderer.
   No framework. No build step.
   ========================================================================== */

(() => {
  "use strict";

  /* ----------------------------------------------------------------------
     1. DATA
     ---------------------------------------------------------------------- */

  const RELATIONSHIPS = [
    { value: "Mother",      label: "Mother",      icon: "🌸" },
    { value: "Father",      label: "Father",      icon: "👔" },
    { value: "Sister",      label: "Sister",      icon: "💫" },
    { value: "Brother",     label: "Brother",     icon: "🎮" },
    { value: "Wife",        label: "Wife",        icon: "💍" },
    { value: "Husband",     label: "Husband",     icon: "🥂" },
    { value: "Girlfriend",  label: "Girlfriend",  icon: "💌" },
    { value: "Boyfriend",   label: "Boyfriend",   icon: "🔥" },
    { value: "Saali",       label: "Saali",       icon: "✨" },
    { value: "Saala",       label: "Saala",       icon: "🤝" },
    { value: "Friend",      label: "Friend",      icon: "🍻" },
    { value: "Boss",        label: "Boss",        icon: "📈" },
    { value: "Colleague",   label: "Colleague",   icon: "💼" },
    { value: "Cousin",      label: "Cousin",      icon: "🎉" },
    { value: "Grandparent", label: "Grandparent", icon: "🫖" },
    { value: "Other",       label: "Other",       icon: "🎁" }
  ];

  const OCCASIONS = [
    { value: "Birthday",        label: "Birthday",        icon: "🎂" },
    { value: "Anniversary",     label: "Anniversary",     icon: "💞" },
    { value: "Diwali",          label: "Diwali",          icon: "🪔" },
    { value: "Raksha Bandhan",  label: "Raksha Bandhan",  icon: "🪢" },
    { value: "Karwa Chauth",    label: "Karwa Chauth",    icon: "🌙" },
    { value: "Wedding",         label: "Wedding",         icon: "💒" },
    { value: "Holi",            label: "Holi",            icon: "🌈" },
    { value: "Eid",             label: "Eid",             icon: "🌜" },
    { value: "Christmas",       label: "Christmas",       icon: "🎄" },
    { value: "House Warming",   label: "House Warming",   icon: "🏡" },
    { value: "Promotion",       label: "Promotion",       icon: "🚀" },
    { value: "Just Because",    label: "Just Because",    icon: "🎈" }
  ];

  const BUDGET_HINTS = [
    { upto: 1000,     text: "Chocolates, flowers, small hampers" },
    { upto: 3000,     text: "Accessories, books, grooming sets" },
    { upto: 7000,     text: "Apparel, fragrances, kitchen gadgets" },
    { upto: 15000,    text: "Smartwatches, audio, premium hampers" },
    { upto: 30000,    text: "Tablets, gold coins, statement jewellery" },
    { upto: Infinity, text: "Luxury watches, electronics, experiences" }
  ];

  const TYPE_GLYPHS = {
    Formal:      "👔",
    Funky:       "🎨",
    Romantic:    "💝",
    Practical:   "🧰",
    Traditional: "🪔",
    Luxury:      "💎",
    default:     "🎁"
  };

  /* ----------------------------------------------------------------------
     2. STATE
     ---------------------------------------------------------------------- */

  const state = {
    step: 0,
    relationship: "",
    occasion: "",
    age_group: "",
    gender: "",
    vibe: "",
    budget: 2500,
    notes: "",
    city: "",
    gift_types: ["Formal", "Funky", "Romantic", "Practical", "Traditional", "Luxury"],
    saved: loadSaved()
  };

  function loadSaved() {
    try { return JSON.parse(localStorage.getItem("gg_saved") || "[]"); }
    catch { return []; }
  }
  function persistSaved() {
    try { localStorage.setItem("gg_saved", JSON.stringify(state.saved)); }
    catch { /* quota exceeded */ }
  }

  /* ----------------------------------------------------------------------
     3. DOM REFS
     ---------------------------------------------------------------------- */

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  const els = {
    hero:           $("#hero"),
    wizard:         $("#wizard"),
    loading:        $("#loading"),
    results:        $("#results"),
    errstate:       $("#errstate"),
    startBtn:       $("#startBtn"),
    pillsRel:       $("#pillsRelationship"),
    pillsOcc:       $("#pillsOccasion"),
    chipsAge:       $("#chipsAge"),
    chipsGender:    $("#chipsGender"),
    chipsVibe:      $("#chipsVibe"),
    step3Next:      $("#step3Next"),
    budgetSlider:   $("#budget"),
    budgetValue:    $("#budgetValue"),
    budgetHint:     $("#budgetHint"),
    notes:          $("#notes"),
    notesCount:     $("#notesCount"),
    city:           $("#city"),
    submitBtn:      $("#submitBtn"),
    loadingPhase:   $("#loadingPhase"),
    resultsGrid:    $("#resultsGrid"),
    rsRelationship: $("#rsRelationship"),
    rsOccasion:     $("#rsOccasion"),
    rsBudget:       $("#rsBudget"),
    thinkingText:   $("#thinkingText"),
    proTip:         $("#proTip"),
    proTipText:     $("#proTipText"),
    refineBtn:      $("#refineBtn"),
    shareBtn:       $("#shareBtn"),
    fab:            $("#fab"),
    fabBadge:       $("#fabBadge"),
    errstateText:   $("#errstateText"),
    retryBtn:       $("#retryBtn"),
    wizardProgress: $("#wizardProgress")
  };

  /* ----------------------------------------------------------------------
     4. INIT — populate pill grids
     ---------------------------------------------------------------------- */

  function renderPills(container, items, key) {
    container.innerHTML = items.map(it => `
      <button type="button" class="pill"
              data-key="${key}" data-value="${escapeAttr(it.value)}"
              aria-pressed="false">
        <span class="pill-icon" aria-hidden="true">${it.icon}</span>
        <span class="pill-label">${escapeHtml(it.label)}</span>
      </button>
    `).join("");
  }

  renderPills(els.pillsRel, RELATIONSHIPS, "relationship");
  renderPills(els.pillsOcc, OCCASIONS,     "occasion");

  /* ----------------------------------------------------------------------
     5. STEP NAVIGATION
     ---------------------------------------------------------------------- */

  function showStep(n, opts) {
    opts = opts || {};
    state.step = n;

    [els.hero, els.wizard, els.loading, els.results, els.errstate].forEach(el => {
      if (el) el.hidden = true;
    });

    let focusTarget = null;

    if (n === 0) {
      els.hero.hidden = false;
      focusTarget = $(".hero-headline", els.hero);
    } else if (n >= 1 && n <= 5) {
      els.wizard.hidden = false;
      $$(".wizard-step", els.wizard).forEach(s => {
        s.hidden = parseInt(s.dataset.step, 10) !== n;
      });
      updateProgressDots(n);
      const active = $(`.wizard-step[data-step="${n}"]`);
      if (active) {
        active.style.animation = "none";
        void active.offsetWidth;
        active.style.animation = "";
        focusTarget = $(".wizard-question", active);
      }
    } else if (n === 6) {
      els.loading.hidden = false;
      focusTarget = $(".loading-headline", els.loading);
    } else if (n === 7) {
      els.results.hidden = false;
      focusTarget = $(".results-title", els.results);
    } else if (n === 8) {
      els.errstate.hidden = false;
      focusTarget = $("h2", els.errstate);
    }

    window.scrollTo({ top: 0, behavior: "instant" });

    if (focusTarget && !opts.skipFocus) {
      try { focusTarget.focus({ preventScroll: true }); } catch { /* no-op */ }
    }

    syncHash(n, opts.replace);
  }

  function updateProgressDots(activeStep) {
    if (!els.wizardProgress) return;
    $$(".progress-dot", els.wizardProgress).forEach(dot => {
      const n = parseInt(dot.dataset.dot, 10);
      dot.classList.remove("active", "done");
      if (n === activeStep) dot.classList.add("active");
      else if (n < activeStep) dot.classList.add("done");
    });
  }

  function syncHash(n, replace) {
    const hash =
      n === 0 ? "" :
      (n >= 1 && n <= 5) ? `#step-${n}` :
      n === 7 ? "#results" :
      n === 8 ? "#error" :
      "";
    const want = hash || location.pathname;
    if (location.hash === hash || (hash === "" && !location.hash)) return;
    if (replace) history.replaceState(null, "", want);
    else         history.pushState(null, "", want);
  }

  function advance() {
    const next = Math.min(state.step + 1, 5);
    showStep(next);
  }
  function goBack() {
    if (state.step === 8 || state.step === 7) return showStep(5);
    if (state.step <= 1) return showStep(0);
    showStep(state.step - 1);
  }

  /* ----------------------------------------------------------------------
     6. PILL / CHIP HANDLERS
     ---------------------------------------------------------------------- */

  function setSelected(group, value) {
    $$("button", group).forEach(btn => {
      const isMatch = btn.dataset.value === value;
      btn.setAttribute("aria-pressed", isMatch ? "true" : "false");
    });
  }

  function pillClick(e) {
    const btn = e.target.closest(".pill");
    if (!btn) return;
    state[btn.dataset.key] = btn.dataset.value;
    setSelected(btn.parentElement, btn.dataset.value);
    setTimeout(() => advance(), 180);
  }

  els.pillsRel.addEventListener("click", pillClick);
  els.pillsOcc.addEventListener("click", pillClick);

  els.chipsAge.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    state.age_group = btn.dataset.value;
    setSelected(els.chipsAge, btn.dataset.value);
    maybeEnableStep3Next();
  });

  els.chipsGender.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    const value = btn.dataset.value;
    state.gender = value === "__skip__" ? "" : value;
    setSelected(els.chipsGender, value);
    maybeEnableStep3Next();
  });

  els.chipsVibe.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    state.vibe = btn.dataset.value;
    setSelected(els.chipsVibe, btn.dataset.value);
    maybeEnableStep3Next();
  });

  function maybeEnableStep3Next() {
    els.step3Next.disabled = !(state.age_group && state.vibe);
  }

  /* ----------------------------------------------------------------------
     7. STEP 4 — BUDGET
     ---------------------------------------------------------------------- */

  function formatBudget(n) {
    if (n >= 1000) return "₹" + n.toLocaleString("en-IN");
    return "₹" + n;
  }

  function updateBudgetUI() {
    els.budgetValue.textContent = formatBudget(state.budget);
    const hint = BUDGET_HINTS.find(h => state.budget <= h.upto);
    els.budgetHint.textContent = hint ? hint.text : BUDGET_HINTS[0].text;
  }

  els.budgetSlider.addEventListener("input", (e) => {
    state.budget = parseInt(e.target.value, 10);
    updateBudgetUI();
  });

  /* ----------------------------------------------------------------------
     8. STEP 5 — NOTES + CITY
     ---------------------------------------------------------------------- */

  els.notes.addEventListener("input", (e) => {
    state.notes = e.target.value;
    els.notesCount.textContent = String(e.target.value.length);
  });

  if (els.city) {
    els.city.addEventListener("input", (e) => {
      state.city = e.target.value.trim().slice(0, 50);
    });
  }

  /* ----------------------------------------------------------------------
     9. SUBMIT
     ---------------------------------------------------------------------- */

  async function submit() {
    showStep(6);

    const phases = [
      "Thinking about what they'd love…",
      "Matching gifts to the occasion…",
      "Writing the perfect reasons…"
    ];
    let phaseIdx = 0;
    els.loadingPhase.textContent = phases[0];
    const phaseInterval = setInterval(() => {
      phaseIdx = (phaseIdx + 1) % phases.length;
      els.loadingPhase.textContent = phases[phaseIdx];
    }, 1800);

    try {
      const payload = {
        relationship: state.relationship,
        occasion:     state.occasion,
        age_group:    state.age_group,
        vibe:         state.vibe,
        budget:       state.budget,
        gender:       state.gender,
        notes:        state.notes,
        city:         state.city,
        gift_types:   state.gift_types
      };

      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      clearInterval(phaseInterval);

      if (!res.ok) throw new Error(`API ${res.status}`);
      const data = await res.json();
      renderResults(data);
      showStep(7);
    } catch (err) {
      clearInterval(phaseInterval);
      console.error("Submit failed:", err);
      els.errstateText.textContent = "Please try again in a moment.";
      showStep(8);
    }
  }

  els.retryBtn.addEventListener("click", submit);

  const step5Form = $("#step5Form");
  if (step5Form) {
    step5Form.addEventListener("submit", (e) => {
      e.preventDefault();
      submit();
    });
  }

  $$('[data-action="submit"]').forEach(b => b.addEventListener("click", submit));

  /* ----------------------------------------------------------------------
     10. RESULTS RENDER
     ---------------------------------------------------------------------- */

  function renderResults(data) {
    els.rsRelationship.textContent = (state.relationship || "friend").toLowerCase();
    els.rsOccasion.textContent     = state.occasion || "this occasion";
    els.rsBudget.textContent       = formatBudget(state.budget) + " budget";
    els.thinkingText.textContent   = data.thinking_trace || "";

    if (data.pro_tip) {
      els.proTipText.textContent = data.pro_tip;
      els.proTip.hidden = false;
    } else {
      els.proTip.hidden = true;
    }

    const recs = (data.recommendations || []).slice(0, 10);
    els.resultsGrid.innerHTML = recs.map((r, i) => productCard(r, i)).join("");

    $$(".heart", els.resultsGrid).forEach(btn => {
      btn.addEventListener("click", () => toggleSave(btn));
    });

    updateFab();
  }

  function productCard(r, i) {
    const id       = r.id ?? (i + 1);
    const title    = r.title || "Gift";
    const giftType = r.gift_type || "default";
    const glyph    = r.icon || TYPE_GLYPHS[giftType] || TYPE_GLYPHS.default;
    const price    = r.approx_price_inr || formatBudget(state.budget);
    const why      = r.why_applicable || r.description || "";
    const links    = r.purchase_links || {};
    const { primary, secondary } = pickLinks(links, title);
    const isSaved  = state.saved.some(s => s.id === id);
    const animDelay = (i * 55) + "ms";

    const secondaryBtn = secondary
      ? `<a class="btn-buy btn-buy-secondary"
            href="${escapeAttr(secondary.url)}"
            target="_blank" rel="noopener nofollow sponsored">
           ${escapeHtml(secondary.label)}
         </a>`
      : "";

    return `
      <article class="product-card" style="animation-delay:${animDelay}">
        <div class="card-top">
          <div class="card-icon-wrap" aria-hidden="true">${glyph}</div>
          <div class="card-body">
            <span class="card-type-tag">${escapeHtml(giftType)}</span>
            <h3 class="card-title">${escapeHtml(title)}</h3>
            <div class="card-price">${escapeHtml(price)}</div>
          </div>
        </div>
        <p class="card-why">${escapeHtml(why)}</p>
        <div class="card-actions">
          <a class="btn-buy btn-buy-primary"
             href="${escapeAttr(primary.url)}"
             target="_blank" rel="noopener nofollow sponsored">
            Buy on ${escapeHtml(primary.label)}
          </a>
          ${secondaryBtn}
          <button type="button" class="heart"
                  aria-label="Save ${escapeAttr(title)}"
                  aria-pressed="${isSaved ? "true" : "false"}"
                  data-id="${id}"
                  data-title="${escapeAttr(title)}"
                  data-url="${escapeAttr(primary.url)}">
            <svg width="20" height="20" viewBox="0 0 24 24"
                 fill="${isSaved ? "currentColor" : "none"}"
                 stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </button>
        </div>
      </article>`;
  }

  function isSafeHttpUrl(url) {
    try {
      const u = new URL(url, location.origin);
      return u.protocol === "http:" || u.protocol === "https:";
    } catch { return false; }
  }

  const LINK_ORDER = [
    ["amazon",       "Amazon"],
    ["flipkart",     "Flipkart"],
    ["myntra",       "Myntra"],
    ["shoppersstop", "Shoppers Stop"],
    ["meesho",       "Meesho"],
    ["blinkit",      "Blinkit"]
  ];

  function pickLinks(links, title) {
    const valid = LINK_ORDER
      .map(([k, label]) => {
        const url = links[k];
        return (url && isSafeHttpUrl(url)) ? { url, label } : null;
      })
      .filter(Boolean);

    const primary = valid[0] || {
      url: "https://www.amazon.in/s?k=" + encodeURIComponent(title),
      label: "Amazon"
    };
    const secondary = valid[1] || null;
    return { primary, secondary };
  }

  /* ----------------------------------------------------------------------
     11. SAVE / FAB / SHARE
     ---------------------------------------------------------------------- */

  function toggleSave(btn) {
    const id    = parseInt(btn.dataset.id, 10);
    const title = btn.dataset.title;
    const url   = btn.dataset.url;
    const idx   = state.saved.findIndex(s => s.id === id);

    if (idx >= 0) {
      state.saved.splice(idx, 1);
      btn.setAttribute("aria-pressed", "false");
      btn.querySelector("svg").setAttribute("fill", "none");
    } else {
      state.saved.push({ id, title, url, ts: Date.now() });
      btn.setAttribute("aria-pressed", "true");
      btn.querySelector("svg").setAttribute("fill", "currentColor");
    }
    persistSaved();
    updateFab();
  }

  function updateFab() {
    const n = state.saved.length;
    els.fab.hidden = n === 0;
    els.fabBadge.textContent = String(n);
  }

  els.fab.addEventListener("click", () => {
    if (!state.saved.length) return;
    const lines = state.saved.map(s => `${s.title}\n${s.url}`).join("\n\n");
    sharePayload({
      title: "My gift shortlist",
      text: `My GiftingGenie shortlist:\n\n${lines}\n\nhttps://gifting-idea.vercel.app`
    });
  });

  els.shareBtn.addEventListener("click", () => {
    sharePayload({
      title: "GiftingGenie",
      text: `Found gift ideas for my ${state.relationship} for ${state.occasion} on GiftingGenie.`,
      url: location.href
    });
  });

  function sharePayload(payload) {
    if (navigator.share) {
      navigator.share(payload).catch(() => fallbackCopy(payload));
    } else {
      fallbackCopy(payload);
    }
  }

  function fallbackCopy(payload) {
    const text = [payload.title, payload.text, payload.url].filter(Boolean).join("\n");
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => toast("Copied to clipboard!"));
    } else {
      alert(text);
    }
  }

  function toast(msg) {
    const t = document.createElement("div");
    t.className = "genie-toast";
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2600);
  }

  /* ----------------------------------------------------------------------
     12. NAVIGATION GLUE
     ---------------------------------------------------------------------- */

  els.startBtn.addEventListener("click", () => showStep(1));
  $$('[data-action="back"]').forEach(b => b.addEventListener("click", goBack));
  $$('[data-action="next"]').forEach(b => b.addEventListener("click", advance));
  els.refineBtn.addEventListener("click", () => showStep(1));

  window.addEventListener("popstate", () => {
    const m = location.hash.match(/^#step-([1-5])$/);
    if (m) showStep(parseInt(m[1], 10), { replace: true });
    else if (!location.hash) showStep(0, { replace: true });
    else if (location.hash === "#results" || location.hash === "#error") {
      showStep(0, { replace: true });
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && state.step >= 1 && state.step <= 5) goBack();
  });

  /* ----------------------------------------------------------------------
     13. UTILITIES
     ---------------------------------------------------------------------- */

  function escapeHtml(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
  function escapeAttr(s) { return escapeHtml(s); }

  /* ----------------------------------------------------------------------
     14. BOOT
     ---------------------------------------------------------------------- */

  updateBudgetUI();
  updateFab();

  const m = location.hash.match(/^#step-([1-5])$/);
  if (m) showStep(parseInt(m[1], 10), { replace: true, skipFocus: true });
  else showStep(0, { replace: true, skipFocus: true });

})();
