# RR Track Research

Athlete research spreadsheet for **Coach Hayden Cox** at **Railroad Athletics**.

**Live:** [rr-track-research.vercel.app](https://rr-track-research.vercel.app)

## What This Is

A sortable, filterable database of 102 U.S. women's distance runners who competed at USATF Outdoor Championships or Olympic Trials (2022–2025). Qualifying thresholds:

- **5K:** sub-15:45
- **Steeplechase:** sub-10:15
- **10K:** sub-33:30

## Features

- Sort by any column (click headers)
- Filter by event or search by name/college/IG
- **Star athletes** — click ★ to favorite, filter to starred only
- **Notes** — click the doc icon to add private notes per athlete
- Stars and notes persist in the browser via localStorage (no backend)

## Data Fields

| Column | Source |
|--------|--------|
| Name / Maiden | World Athletics profiles |
| Age | As of April 2026 |
| College | TFRRS records |
| 5K / SC / 10K PBs | WA annual top lists (2022–2026) |
| USAs Events | USATF championship results |
| Instagram | Manual lookup |

## Tech

Single static HTML file. No build system, no dependencies. Inline CSS + JS. Deployed to Vercel via GitHub auto-deploy.

## Repo

- `index.html` — the entire app
- `rr-logo.png` — Railroad Athletics logo
