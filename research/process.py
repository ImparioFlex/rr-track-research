#!/usr/bin/env python3
"""Filter WA top lists for sub-33:30 USA women 10K, dedupe across 2022-2026, exclude existing 102."""
import json
import re
import unicodedata

YEARS = [2022, 2023, 2024, 2025, 2026]
THRESHOLD_SEC = 33 * 60 + 30  # 33:30.00

# Existing 102 names — normalized for matching
EXISTING_RAW = """Alicia Monson, Josette Andrews (née Norris), Elle St. Pierre (née Purrier), Weini Kelati, Karissa Schweizer, Elise Cranny, Shelby Houlihan, Elly Henes, Whittni Morgan (née Orton), Courtney Frerichs, Bailey Hertenstein, Courtney Wayment, Taylor Roe, Ella Donaghu, Emily Infeld, Parker Valby, Natosha Rogers, Lexy Halladay (Halladay-Lowry), Grace Hartman, Emily Venters, Annie Rodenfels, Allie Buchalski, Fiona O'Keeffe, Amanda Vestri, Katelyn Tuohy, Taylor Werner, Abby Nichols, Rachel Smith (née Schneider), Vanessa Fraser, Lucy Jenks (née Nodler), Chloe Scrimgeour, Katie Camarena, Bethany Hasz, Kayley DeLay, Amaris Tyynismaa, Sophia Kennedy, Emily Lipari, Elise Stearns, Katie Wasserman, Sarah Lancaster, Jessica McClain (née Tonn), Katie Izzo, Abbey Cooper (née D'Agostino), Ednah Kurgat, Gabrielle Jennings, Olivia Markezich, Maggie Montoya, Kaylee Mitchell, Eleanor Fulton, Paige Stoner, Lauren Gregory, Hannah Steelman, Erika Kemp, Molly Born, Kellyn Taylor (née Johnson), Molly Grabill, Katrina Coogan, Madie Boreman, Jennifer Randall, Elizabeth Leachman, Susanna Sullivan, Jenna Magness, Allie Ostrander, Savannah Shaw, Logan Jolly (née Morris), Maddie Alm, Carrie Verdon, Marielle Hall, Claire Green, Olivia Pratt, Carmen Graves, Val Constien, Angelina Ellis, Anne-Marie Blaney, Stephanie Bruce (née Rothstein), Cailie Logue Hughes, Makena Morley, Kassie Parker, Amy Davis-Green (née Davis), Sophie Novak, Calli Doan, Anna Oeser, Angelina Napoleon, Jessica Gockley-Day (née Gockley), Gracie Hyde, Katie Rainsberger, Emma Coburn, Marisa Howard, Kristlin Gear, Colleen Quigley, Taylor Lovell, Emma Gee, Janette Schraft, Colett Rampf, Karrie Baloga, Maggie Liebich, Abby Kohut-Jackson, Keira D'Amato, Emily Durgin, Millie Paladino, Caroline Sang, Jeralyn Poe"""


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm_token(s):
    """Normalize a single token for matching: lower, strip accents, strip punctuation."""
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z]", "", s)
    return s


def parse_existing(raw):
    """Return set of exact (first_norm, last_norm) pairs (incl maiden alts)."""
    pairs = set()
    raw_names = []
    for chunk in raw.split(","):
        name = chunk.strip()
        # capture "(née X)" / "(X-Y)" alt
        alt = None
        m = re.search(r"\(n[eé]e\s+([^)]+)\)", name)
        if m:
            alt = m.group(1).strip()
        m2 = re.search(r"\(([^)]+)\)", name)
        if m2 and not m:
            alt = m2.group(1).strip()
        primary = re.sub(r"\s*\([^)]*\)", "", name).strip()
        raw_names.append(primary)
        toks = primary.split()
        if len(toks) >= 2:
            first = norm_token(toks[0])
            last = norm_token(toks[-1])
            # also second-to-last (for compound surnames like "Cailie Logue Hughes" — "Logue" is also surname)
            pairs.add((first, last))
            if len(toks) >= 3:
                pairs.add((first, norm_token(toks[-2])))
        # alt form
        if alt:
            alt_clean = alt.strip()
            alt_parts = re.split(r"[-\s]+", alt_clean)
            first_primary = toks[0] if toks else ""
            for ap in alt_parts:
                if ap:
                    pairs.add((norm_token(first_primary), norm_token(ap)))
    return pairs, raw_names


def parse_wa_name(raw):
    """WA cell looks like 'First LAST' or 'First Middle LAST LAST'. Return cleaned name + (first, last) tokens."""
    raw = raw.strip()
    tokens = raw.split()
    # find ALL-CAPS surname tokens (contiguous tail)
    last_tokens = []
    while tokens and tokens[-1].isupper() and len(tokens[-1]) > 1:
        last_tokens.insert(0, tokens.pop())
    first_tokens = tokens
    # title-case with Mc/Mac/O' awareness
    def tc_part(p):
        if not p:
            return p
        # apostrophe: capitalize after apostrophe ("o'shea" -> "O'Shea")
        if "'" in p:
            return "'".join(seg[:1].upper() + seg[1:].lower() if seg else seg for seg in p.split("'"))
        # Mc / Mac prefix: "mcclain" -> "McClain", "mcdonald" -> "McDonald"
        low = p.lower()
        if low.startswith("mc") and len(p) > 2:
            return "Mc" + p[2:3].upper() + p[3:].lower()
        if low.startswith("mac") and len(p) > 3 and p[3:].lower() not in ("hu",):
            # be conservative: only apply if known surname pattern - skip generic
            return p[:1].upper() + p[1:].lower()
        return p[:1].upper() + p[1:].lower()
    def tc(s):
        return "-".join(tc_part(p) for p in s.split("-"))
    first_clean = " ".join(tc(t) for t in first_tokens)
    last_clean = " ".join(tc(t) for t in last_tokens)
    cleaned = (first_clean + " " + last_clean).strip()
    first_n = norm_token(first_tokens[0]) if first_tokens else ""
    last_n = norm_token(last_tokens[-1]) if last_tokens else ""
    return cleaned, first_n, last_n, [norm_token(t) for t in last_tokens]


def time_to_sec(s):
    m = re.match(r"^(\d+):(\d+\.\d+)$", s.strip())
    if not m:
        return None
    return int(m.group(1)) * 60 + float(m.group(2))


def main():
    existing_pairs, existing_raw = parse_existing(EXISTING_RAW)
    print(f"existing: {len(existing_raw)} names, {len(existing_pairs)} match keys")

    # collect: athlete_key -> (best_sec, best_mark_str, name, href, year, nat)
    best = {}
    for y in YEARS:
        with open(f"wa_{y}.json") as fh:
            rows = json.load(fh)
        for r in rows:
            cells = r["cells"]
            # cells: [rank, mark, ?, name, dob, nat, ...]
            if len(cells) < 6:
                continue
            mark = cells[1]
            name_raw = cells[3]
            nat = cells[5]
            sec = time_to_sec(mark)
            if sec is None:
                continue
            if sec >= THRESHOLD_SEC:
                continue
            # filter: nationality must be USA
            if nat.strip().upper() != "USA":
                continue
            cleaned, first_n, last_n, all_last_n = parse_wa_name(name_raw)
            href = r.get("href", "")
            key = (first_n, last_n)
            if key not in best or sec < best[key][0]:
                best[key] = (sec, mark, cleaned, href, y, nat, all_last_n, first_n, last_n)

    print(f"distinct sub-33:30 USA athletes (raw): {len(best)}")

    # dedupe vs existing
    new_athletes = []
    excluded = []
    review = []
    for key, (sec, mark, name, href, year, nat, all_last_n, first_n, last_n) in best.items():
        # match: exact (first, last) for any of athlete's last-name tokens
        matched = False
        for ln in all_last_n:
            if (first_n, ln) in existing_pairs:
                matched = True
                break
        if matched:
            excluded.append((name, mark, year))
        else:
            new_athletes.append({
                "name": name,
                "tenk": mark,
                "wa_url": ("https://worldathletics.org" + href) if href else "",
                "_year": year,
                "_sec": sec,
            })

    new_athletes.sort(key=lambda x: x["_sec"])
    print(f"\nEXCLUDED (matched existing 102): {len(excluded)}")
    for n, m, y in sorted(excluded, key=lambda x: x[1]):
        print(f"  {m}  {n}  ({y})")

    print(f"\nNEW: {len(new_athletes)}")
    for a in new_athletes:
        print(f"  {a['tenk']}  {a['name']}  ({a['_year']})  {a['wa_url']}")

    # Strip helper fields for output
    output = [{"name": a["name"], "tenk": a["tenk"], "wa_url": a["wa_url"]} for a in new_athletes]
    with open("new_athletes.json", "w") as fh:
        json.dump(output, fh, indent=2)
    print(f"\nwrote new_athletes.json with {len(output)} entries")


if __name__ == "__main__":
    main()
