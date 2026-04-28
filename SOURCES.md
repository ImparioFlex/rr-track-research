# Data Sources & Reference Links

This is the master reference for everything that feeds the U.S. women's distance research tool. Anything we look up should land here so we never have to rebuild this trail from memory again.

---

## 1. World Athletics annual top lists (PBs)

WA pages are JS-rendered. SSR HTML usually has the table; if not, fall back to the **playwright MCP browser** to grab `<tbody>` rows. The eventId in the URL **overrides the URL path** — verify by checking sample times in the result table.

### Confirmed eventIds (women, outdoor, senior)

| Event | eventId |
|---|---|
| 5000m | `10229514` |
| 3000m steeplechase | `10229524` |
| 10,000m | `10229521` |

### URL templates (replace `{year}` with 2022, 2023, 2024, 2025, 2026)

**5000m**
```
https://worldathletics.org/records/toplists/middlelong/5000-metres/all/women/senior/{year}?regionType=countries&region=usa&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229514&ageCategory=senior
```

**3000m steeplechase**
```
https://worldathletics.org/records/toplists/middlelong/3000-metres-steeplechase/all/women/senior/{year}?regionType=countries&region=usa&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229524&ageCategory=senior
```

**10,000m**
```
https://worldathletics.org/records/toplists/middlelong/10000-metres/all/women/senior/{year}?regionType=countries&region=usa&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229521&ageCategory=senior
```

**Important query params**
- `regionType=countries&region=usa` — filter to U.S. athletes only
- `bestResultsOnly=true` — one row per athlete (her best mark for that year)
- `maxResultsByCountry=all` — no truncation
- Each year returns up to 100 rows. Check the slowest mark on a year's page; if it's faster than your threshold, paginate. (For our 5K/SC/10K thresholds, page 1 was always sufficient.)

### Athlete profile URLs (for DOB / age)

Two formats both resolve:
```
https://worldathletics.org/athletes/united-states/{slug}-{id}
https://worldathletics.org/athletes/athlete={id}
```

The trailing numeric ID is the WA athlete ID — useful as a stable dedupe key across name changes (married/maiden, typos).

---

## 2. USATF / Olympic Trials results (criterion B starts)

### Primary search

```
site:results.usatf.org USATF Outdoor Championships {year}
site:results.usatf.org Olympic Team Trials 2024
```

The official USATF results host is patchy. In practice, **FlashResults** has cleaner per-event start lists / heat sheets:

| Year | URL |
|---|---|
| 2022 USATF Outdoor | https://www.flashresults.com/2022_Meets/Outdoor/06-23_USATF/ |
| 2023 USATF Outdoor | https://www.flashresults.com/2023_Meets/Outdoor/07-06_USATF/ |
| 2024 Olympic Trials | World Athletics calendar/results, eventId `7209387`; or FlashResults `2024_Meets/Outdoor/06-21_USATF` |
| 2025 USATF Outdoor | Watch Athletics pages: 6905 (W5K), 6876 (W10K), 6870 (WSC) |

### Notes

- 2022 W 10,000m was held standalone on May 27, 2022 at the **USATF 10,000m Championships** at Hayward Field (paired with the Pre Classic), **not** at the late-June outdoor meet. Treat it as the relevant 10K championship for 2022.
- 2024 was the U.S. Olympic Team Trials – Track & Field (Eugene, June). It replaces the regular USATF Outdoor for that year.
- W 5000m / W 3000mSC sometimes have prelim heats + final; W 10,000m is usually a straight final.
- DNS (did not start) and DNF (did not finish) both count as "made the field" for our purposes.

### Wikipedia fallback

```
https://en.wikipedia.org/wiki/{year}_USA_Outdoor_Track_and_Field_Championships
https://en.wikipedia.org/wiki/2024_United_States_Olympic_trials_(track_and_field)
```

Each meet's page has a results table per event, easy to parse.

---

## 3. College affiliation — TFRRS

```
https://www.tfrrs.org
```

- Search by athlete name. Each profile lists her team / school.
- Transfer history isn't always shown on the profile; cross-check via Athletic.net or the school's roster page if needed.
- For non-collegiate athletes (post-grad / international / pre-college), TFRRS won't have a meaningful entry — fall back to LetsRun, the athlete's IG bio, or sponsor page.

---

## 4. Instagram handles

Search pattern that works:
```
"{Full Name}" instagram track {school or sponsor}
```

**Always verify** the handle by inspecting the bio for school/event/sponsor match. Common-name false positives are frequent (e.g. multiple Sarah Carters on IG). If unsure, leave blank rather than guess.

---

## 5. Athlete eligibility / nationality

When a name on a U.S. WA top list looks ambiguous (foreign-origin name, transfer student, naturalized), verify before adding:

- WA profile shows "Nationality: United States" — that's the primary check.
- If she ever competed for another country at a major championship, double-check her current eligibility (WA records the most recent country switch).
- Athletes flagged in this project so far: Brighter Jepchumba, Lucy Ndungu, Florance Uwajeneza.

---

## 6. Naming aliases used in this dataset

Maiden / married / nickname / typo collapses applied during merge. Source of truth for canonical name choice is whichever form appears on Coach Hayden Cox's existing 102-name list; otherwise use the most common public form.

| Variant | Canonical |
|---|---|
| Andrea Rodenfels | Annie Rodenfels |
| Gabbi Jennings | Gabrielle Jennings |
| Krissy Gear | Kristlin Gear |
| Lexy Halladay-Lowry | Lexy Halladay |
| Lucy Nodler Jenks | Lucy Jenks |
| Cailie Hughes | Cailie Logue Hughes |
| Margaret Liebich | Maggie Liebich |
| Sam Nadel | Samantha Nadel |
| Kasandra Parker | Kassie Parker |
| Jackie Gaughan | Jacqueline Gaughan |
| Sydney Vaught | Sydney Thorvaldson (married) |
| Danielle Polerecky | Danielle Shanahan |
| Raygan Peterson | Raygan Dimond (married) |
| Lauren Goss | Lauren Hurley (married) |
| Anna Camp | Anna Camp Bennett |
| Josette Norris | Josette Andrews (married) |
| Whittni Orton | Whittni Morgan (married) |
| Rachel Schneider | Rachel Smith (married) |
| Lucy Nodler | Lucy Jenks (married) |
| Jessica Tonn | Jessica McClain (married) |
| Abbey D'Agostino | Abbey Cooper (married) |
| Kellyn Johnson | Kellyn Taylor (married) |
| Logan Morris | Logan Jolly (married) |
| Stephanie Rothstein | Stephanie Bruce (married) |
| Amy Davis | Amy Davis-Green (married) |
| Jessica Gockley | Jessica Gockley-Day (married) |
| Cailie Logue | Cailie Logue Hughes (married) |
| Valerie Constien | Val Constien |
| Weini Kelati Frezghi | Weini Kelati |
| Elena Henes | Elly Henes |
| Katie Thronson | Katherine Thronson |

(Maintained in `research/merge_all.py` `ALIASES` dict.)

---

## 7. Selection criteria

Athlete is included in the master list if **either** is true:

- **(A)** PB at any point 2022 onward of: **sub-15:45 5000m**, OR **sub-10:15 3000mSC**, OR **sub-33:30 10,000m** (track only).
- **(B)** Started in W 5000m / W 3000mSC / W 10,000m at USATF Outdoor Championships or the U.S. Olympic Team Trials in 2022, 2023, 2024, or 2025 (including DNS/DNF).

Excludes: 1500m / mile / marathon-only specialists; non-U.S. athletes (even on U.S. lists); relay-only entries.

---

## 8. Files in `research/`

| File | What it is |
|---|---|
| `wa_5k_new.json` | 100 sub-15:45 5K athletes new to the existing 102 list |
| `wa_sc_new.json` | 132 sub-10:15 SC athletes new to the existing 102 list |
| `wa_10k_new.json` | 160 sub-33:30 10K athletes new to the existing 102 list |
| `wa_merged_new.json` | The above three deduped by WA athlete ID into 342 unique |
| `wa_2022.json` … `wa_2026.json` | Raw 10K-only WA scrape per year (audit trail) |
| `usas_starters.json` | 134 USAs / OT W 5K/SC/10K starters across 2022–2025 |
| `enrich_chunk_{1..5}.json` | Worklists for the 5-way parallel enrichment pass |
| `enrich_chunk_{1..5}_out.json` | Enriched outputs (age/college/IG filled) |
| `wa_merged_full.json` | Final unified DATA — 447 athletes, ready for index.html |
| `merge.py` | Script: dedupe the 3 WA event lists by WA athlete ID |
| `merge_all.py` | Script: build the unified DATA (existing + WA + USAs) with alias map |
| `inject.py` | Script: replace the `DATA = [...]` block in `index.html` |
| `process.py` | Original 10K parser (artifact from agent run) |

To rebuild from scratch:

```bash
cd "/Users/trevor/Projects/CLAUDE/rr-track-research"
python3 research/merge.py        # combine WA event lists
python3 research/merge_all.py    # combine with existing + USAs
python3 research/inject.py       # write back into index.html
```

---

## 9. Tooling notes

- **WebFetch** works for static HTML and SSR-rendered tables. Returns summarized text — fine for short pages, lossy for long tables (the 5K agent caught this and switched to `curl` for raw HTML).
- **Playwright MCP browser** is the fallback when WebFetch can't see JS-rendered tables. Note: only one browser session at a time across agents — concurrent runs will get "Browser is already in use" errors. Stagger if needed.
- `curl` direct fetch works on WA pages because the table is in the SSR HTML; you don't strictly need a browser.
- WebSearch is the right tool for Instagram lookups; it returns the bio snippet which makes verification fast.
