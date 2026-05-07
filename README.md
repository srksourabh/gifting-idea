# GiftingGenie

Indian-context gift recommender. Ask once, get 10 thoughtful suggestions tailored to relationship, occasion, age, vibe, and budget.

**Live:** https://gifting-idea.vercel.app

## Stack

Python 3 on Vercel serverless functions. Google Gemini 1.5 Flash for recommendations. No build step. No framework. Stdlib only.

## Local preview

```sh
npm i -g vercel
vercel env pull .env.local
vercel dev
```

Then open http://localhost:3000.

## What's next (v2)

A v2 rebuild is in progress — real product links via Gemini 2.0 grounded search and a mobile-first wizard UI. See:

- [`docs/PRD.md`](docs/PRD.md) — product requirements
- [`docs/PLAN.md`](docs/PLAN.md) — phased execution plan

## Project notes

See [`CLAUDE.md`](CLAUDE.md) for development conventions and tech-stack honesty.
