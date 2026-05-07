# CLAUDE.md — gifting-idea

Project brief for Claude Code. Global rules in `~/.claude/CLAUDE.md` still apply; this file only adds project-specific facts.

## What this is

GiftingGenie — a single-page web app that recommends Indian-context gifts based on relationship, occasion, age, vibe, and budget. Live at https://gifting-idea.vercel.app.

- **Repo:** https://github.com/srksourabh/gifting-idea
- **Vercel project:** `prj_r6K5mSmOlbbJ92FG4sDg9iJNGMKC` (team `srksourabhs-projects`)
- **Deploy flow:** push to `main` → Vercel auto-deploys (no CI to run locally).

## Tech stack (actual, not what the README says)

- **Runtime:** Python 3, Vercel serverless functions (each file in `api/` is one function).
- **HTTP layer:** `http.server.BaseHTTPRequestHandler` — **NOT FastAPI**, despite `vercel.json` declaring `framework: fastapi` and the README claiming otherwise.
- **Dependencies:** none. `requirements.txt` is just a comment. Stdlib only (`urllib.request` for the Gemini call).
- **AI:** Google Gemini 1.5 Flash via REST. Requires env var `GEMINI_API_KEY`. Falls back to a rule-based recommender if the key is missing.
- **Frontend:** a large HTML/CSS/JS string literal embedded inside `api/index.py`. There is no `static/` directory and no build step.

## File map

| Path | Purpose |
|---|---|
| `api/index.py` | `GET /` — serves the embedded HTML page. ~71 KB; most of it is the inline frontend. |
| `api/recommend.py` | `POST /api/recommend` — calls Gemini, returns 10 gift recommendations + thinking trace + pro tip. |
| `api/favicon.py` | `GET /favicon.ico` — inline SVG. |
| `vercel.json` | Routes `/` → `api/index`, `/api/recommend` → `api/recommend`, `/favicon.ico` → `api/favicon`. |
| `assets/cover.png` | Project cover image. Not served by the app. |
| `docs/PRD.md` | v2 product requirements — marketplace integration via Gemini grounding + mobile-first UI overhaul. |
| `docs/PLAN.md` | v2 phase-by-phase execution plan (companion to PRD). |
| `example_request.json` | Sample POST body for `/api/recommend`, useful for curl smoke tests. |

## Working locally

The Vercel serverless layout doesn't run with plain `python`. To preview locally:

```
npm i -g vercel        # one time
vercel dev             # serves on http://localhost:3000
```

Set `GEMINI_API_KEY` in `.env.local` (Vercel CLI picks it up automatically) or you'll get rule-based output instead of AI output.

Pull the production env to local:
```
vercel env pull .env.local
```

## Conventions specific to this repo

- **One function per file** in `api/`. Each defines `class handler(BaseHTTPRequestHandler)` — Vercel's Python runtime requires that exact name.
- **HTML lives in Python strings (today).** When editing the frontend, you're editing a triple-quoted string in `api/index.py`. Watch out for unescaped apostrophes and `{` / `}` if anyone ever switches to f-strings (history shows this has bitten before — see commit `592e0f2`). Phase 0 of v2 extracts this into `static/`.
- **No tests yet.** Verification is manual: deploy a preview branch and click through the UI.
- **Branch pattern:** Cloud Claude Code sessions auto-create branches like `claude/<task>-<id>`. Locally, use plain descriptive branches. v2 work uses `v2/phase-N` branches.

## v2 in progress

See `docs/PRD.md` and `docs/PLAN.md`. v2 is a phased rebuild — adds Gemini 2.0 grounded search for real product links and a mobile-first wizard UI. Stale FastAPI-era docs and shell scripts have been deleted as of 2026-05-06.

## Useful checks

- Production URL: https://gifting-idea.vercel.app
- Latest deployment & build logs: ask via Vercel MCP (`get_deployment`, `get_deployment_build_logs`) — project ID above.
- `GEMINI_API_KEY` is set in Vercel project env; rule-based fallback path lives in `api/recommend.py` (`call_gemini` returns `None` → fallback).
