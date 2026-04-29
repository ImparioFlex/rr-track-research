# Current State

## Project

- name: RR Track Research (U.S. women's distance research spreadsheet for Coach Hayden Cox at Railroad Athletics)
- app root: `/Users/trevor/Projects/CLAUDE/rr-track-research/`
- live URL: https://rr-track-research.vercel.app
- GitHub: `ImparioFlex/rr-track-research` (push to `main` auto-deploys via Vercel)
- stack: single static `index.html` (inline CSS + JS, no build), `rr-logo.png`
- persistence: localStorage only — stars / notes / excludes / contacted / per-field overrides / user-added athletes

## Current Goal

Tool is in usable shape for Coach Hayden's recruiting research. **447 athletes** loaded, all interactive features (star, exclude, contacted, inline-edit-everything, add-athlete, notes modal, search, sort, filters) shipped and live. No outstanding asks from Hayden yet — waiting on his feedback.

## What Was Last Completed (2026-04-28)

This session went from 102 → 447 athletes plus a full feature pass. Final commits on `main`:

- `1106113` — +89 IG handles (236 → 325)
- `022579a` — +264 ages (210 estimated `~22` style + 54 verified, 99.6% coverage)
- `1ea434a` — expand list to 447 athletes via OR-criteria; enrich with college/age/IG (first pass); add `SOURCES.md` + `research/` audit trail
- `42dcc29` — original v1 README
- `47923b8` — original v1 spreadsheet (102 athletes)

### Feature additions (in `index.html`)
- **Exclude (`✕`) column** next to star — strikethrough + sinks to bottom of every sort. Toggleable.
- **Status column** — inline editable italic-orange cell (`+ status` placeholder). Searchable + sortable.
- **All fields editable except Name** — click any cell, inline input/textarea, Enter or click-away to save, Esc to cancel. Reverting to base value drops the override automatically.
- **+ Add athlete** button + modal — full form with validation, persists to `localStorage.rr-added`.
- **Contacted (`✓`) column** — toggleable orange button + filter option.
- **Filters** — Starred / Contacted / Excluded / event type.
- **Estimated age display** — `~22` with subtle orange tilde + dimmed weight; tooltip "Estimated from class year — click to correct"; manual edits auto-clear the estimate flag.
- **Hero + footer source links** — sources are inline in the page note now (WA top lists per event, FlashResults USATF, TFRRS).

### Data expansion
- Selection criteria changed from AND to **OR**: PB sub-15:45 5K / sub-10:15 SC / sub-33:30 10K (2022–2026) **OR** start at USATF Outdoor / Olympic Trials W 5K/SC/10K (2022–2025).
- Net adds: 342 from WA top lists + 3 USAs criterion-B-only.
- Coverage: 447 athletes / 445 age / 440 college / 325 IG / 135 USAs events.

## What Is In Progress

Nothing actively in flight. Tool is at a clean checkpoint awaiting Hayden's feedback.

## Known limitations

- **2 athletes still missing age**: Haley Anderson, Melissa George (very thin public profiles — likely sub-elite club runners).
- **WA athlete IDs are not stored in DATA** — collapsed during merge. If we later want to dedupe a Trevor-added athlete against the canonical list, we'd have to do it by name. Easy fix: add `wa_id` field to the schema and re-inject.
- **2 borderline US-eligibility flags** (Brighter Jepchumba, Lucy Ndungu/Florance Uwajeneza) — kept on the list, untagged in the UI. Trevor or Hayden may want to manually exclude.
- **Cross-device sync not implemented** — localStorage means edits live in one browser only. Supabase upgrade is the natural next step once Hayden actually wants to share notes/contacts with staff.

## Next 3 Priorities (when Hayden lands feedback)

1. **Apply Hayden's feedback** — anything on column order, what info matters most, missing data points, etc.
2. **Persistence upgrade** — move stars / notes / contacted / overrides to Supabase if multi-device or staff-sharing becomes a need.
3. **Outreach layer** — turn `Contacted` toggle into a multi-state pipeline (queued / DM-sent / replied / interested / nope) if it becomes a recruiting CRM use case.

## Files / structure

```
rr-track-research/
├── index.html             # the entire app (~1300 lines, inline CSS + JS, DATA array)
├── rr-logo.png            # Railroad Athletics logo
├── README.md              # what the tool is + tech notes
├── SOURCES.md             # data source URLs, eventIds, alias map, rebuild commands
├── CURRENT-STATE.md       # this file
└── research/              # full audit trail
    ├── wa_merged_full.json    # source of truth for the 447-athlete master list
    ├── wa_merged_new.json     # the 342 WA-list new athletes (pre-merge with existing)
    ├── wa_5k_new.json         # 100 sub-15:45 5K, deduped vs existing 102
    ├── wa_sc_new.json         # 132 sub-10:15 SC, deduped vs existing 102
    ├── wa_10k_new.json        # 160 sub-33:30 10K, deduped vs existing 102
    ├── usas_starters.json     # 134 USATF/OT starters across 2022–2025
    ├── enrich_chunk_{1..5}_out.json   # college/age/IG first pass (collegiate)
    ├── age_chunk_{1..4}_out.json      # second-pass age estimation (264 athletes)
    ├── ig_chunk_{1..4}_out.json       # second-pass IG enrichment (211 athletes)
    ├── merge.py / merge_all.py        # build wa_merged_full.json from sources
    ├── inject.py              # write DATA array back into index.html
    └── apply_*.py             # plumb chunk outputs into the master JSON
```

To rebuild from scratch:
```bash
python3 research/merge.py        # combine WA event lists
python3 research/merge_all.py    # combine with existing 102 + USAs
python3 research/inject.py       # write back into index.html
```

## Notes For The Next AI Session

- **Read SOURCES.md first** for canonical URLs / eventIds / alias map.
- **Don't re-run scrapers casually** — WA pages are behind Cloudflare WAF, so each scrape requires Playwright to clear it first. The full scrape consumed ~5 background agents this session.
- **Estimated ages display as `~22`** in the UI. The `age_est: true` field on each athlete drives this; it auto-clears when the user manually edits the age.
- **The 5K and 10K WA URLs all share `eventId=10229514` in the URL bar but the SC URL has `10229524`.** The eventId actually matters and overrides the URL path — `10229514` = 5K, `10229521` = 10K, `10229524` = SC. Don't trust Trevor-pasted URLs blindly; always verify the page returns the expected event's times.
- **Multiple agents can't share the Playwright browser at once** ("Browser is already in use" error). Stagger if you need WA scraping in parallel.
- **WebSearch is the right tool for IG handles**, not WebFetch — Google indexes IG bios and returns the snippet, which is what you need to verify a handle.
- All data lives in the page itself (`const DATA = [...]` in index.html) and in `research/wa_merged_full.json`. Both are kept in sync via `inject.py`.
