#!/usr/bin/env python3
"""Build the usas_starters.json from the four USAs/Trials meets 2022-2025."""
import json
from collections import defaultdict

# Each entry: (event_code, year_2digit, name)
entries = []

def add(event, yr, names):
    for n in names:
        entries.append((event, yr, n.strip()))

# ============================================================
# 2022 USATF Outdoor Championships - Eugene
# ============================================================

# Women's 5000m FINAL - June 26, 2022 (straight final)
# 23 finishers + 2 DNS
add("5K", "22", [
    "Elise Cranny", "Karissa Schweizer", "Emily Infeld", "Weini Kelati",
    "Natosha Rogers", "Fiona O'Keeffe", "Sarah Lancaster", "Whittni Morgan",
    "Elly Henes", "Eleanor Fulton", "Ella Donaghu", "Josette Norris",
    "Katelyn Tuohy", "Ednah Kurgat", "Abby Nichols", "Allie Ostrander",
    "Katie Izzo", "Jenna Magness", "Emily Lipari", "Elle St. Pierre",
    "Vanessa Fraser", "Allie Buchalski", "Katrina Coogan",
    # DNS
    "Taryn Rawlings", "Andrea Rodenfels"
])

# Women's 3000m Steeplechase FINAL - June 26, 2022 (straight final)
add("SC", "22", [
    "Emma Coburn", "Courtney Wayment", "Courtney Frerichs", "Gabbi Jennings",
    "Katie Rainsberger", "Andrea Rodenfels", "Carmen Graves", "Val Constien",
    "Madie Boreman", "Kayley Delay", "Logan Jolly", "Abby Kohut-Jackson",
    "Alissa Niggemann",
    # DNS
    "Colleen Quigley"
])

# Women's 10000m - May 27, 2022 (held at Pre Classic / standalone USATF 10000m Champs)
add("10K", "22", [
    "Karissa Schweizer", "Alicia Monson", "Natosha Rogers", "Emily Infeld",
    "Weini Kelati", "Sarah Lancaster", "Stephanie Bruce", "Emily Lipari",
    "Carrie Verdon", "Molly Grabill", "Emily Durgin", "Paige Stoner",
    "Caroline Sang", "Marielle Hall", "Makena Morley", "Ednah Kurgat",
    "Susanna Sullivan", "Jeralyn Poe", "Maddie Alm", "Olivia Pratt"
])

# ============================================================
# 2023 USATF Outdoor Championships - Eugene (July 6-9, 2023)
# ============================================================

# Women's 10000m - July 6, 2023 (straight final)
add("10K", "23", [
    "Elise Cranny", "Alicia Monson", "Natosha Rogers", "Weini Kelati",
    "Karissa Schweizer", "Ednah Kurgat", "Emily Venters", "Amanda Vestri",
    "Kasandra Parker", "Alexandra Hays", "Jackie Gaughan", "Vanessa Fraser",
    "Sam Nadel", "Marybeth Chelanga", "Hannah Branch", "Amaya Noe",
    "India Johnson", "Mackenzie Caldwell",
    # DNF (still started)
    "Madeline Block", "Amelia Paladino",
    # DNS
    "Fiona O'Keeffe"
])

# Women's 3000m Steeplechase - Round 1 (July 7) + Final (July 8) 2023
# Heat 1
add("SC", "23", [
    "Logan Jolly", "Krissy Gear", "Olivia Markezich", "Courtney Wayment",
    "Kayley Delay", "Madeline Strandemo", "Emily Cole", "Katie Thronson",
    "Lydia Olivere", "Abby Kohut-Jackson", "Harper McClain", "Katie Rainsberger",
    # DNS
    "Colleen Quigley"
])
# Heat 2
add("SC", "23", [
    "Emma Coburn", "Kaylee Mitchell", "Marisa Howard", "Gabbi Jennings",
    "Madie Boreman", "Lexy Halladay", "Carmen Graves", "Courtney Frerichs",
    "Emma Gee", "Judi Jones", "Angelina Ellis", "Katelyn Mitchem",
    "Meredith Rizzo"
])

# Women's 5000m - July 9, 2023 (straight final)
add("5K", "23", [
    "Elise Cranny", "Alicia Monson", "Natosha Rogers", "Josette Andrews",
    "Elly Henes", "Whittni Morgan", "Katelyn Tuohy", "Weini Kelati",
    "Emily Infeld", "Abby Nichols", "Allie Buchalski", "Andrea Rodenfels",
    "Ednah Kurgat", "Katie Camarena", "Katie Izzo", "Taylor Werner",
    "Emily Lipari", "Hannah Steelman", "Katie Wasserman", "Anna Oeser",
    "Bethany Hasz", "Maddie Alm",
    # DNS
    "Karissa Schweizer"
])

# ============================================================
# 2024 U.S. Olympic Team Trials - Eugene (June 21-30, 2024)
# ============================================================

# Women's 5000m - Heats June 27, Final June 30
# Heat 1
add("5K", "24", [
    "Elle St. Pierre", "Karissa Schweizer", "Parker Valby", "Whittni Morgan",
    "Allie Buchalski", "Abby Nichols", "Taylor Roe", "Katie Wasserman",
    "Lauren Gregory", "Molly Born", "Chloe Scrimgeour", "Grace Hartman",
    "Bailey Hertenstein", "Savannah Shaw"  # DNF
])
# Heat 2
add("5K", "24", [
    "Elise Cranny", "Ella Donaghu", "Rachel Smith", "Katelyn Tuohy",
    "Josette Andrews", "Emily Infeld", "Abbey Cooper", "Maggie Montoya",
    "Natosha Rogers", "Hannah Steelman", "Bethany Hasz", "Jennifer Randall",
    "Elizabeth Leachman", "Katie Camarena", "Claire Green"
])

# Women's 3000m Steeplechase - Round 1 June 24, Final June 27
# Heat 1
add("SC", "24", [
    "Kaylee Mitchell", "Val Constien", "Courtney Wayment", "Madie Boreman",
    "Angelina Ellis", "Annie Rodenfels", "Logan Jolly", "Carmen Graves",
    "Sophie Novak", "Dana Klein", "Taylor Lovell", "Calli Doan",
    "Katherine Thronson", "Emma Gee"
])
# Heat 2
add("SC", "24", [
    "Gabbi Jennings", "Marisa Howard", "Olivia Markezich", "Lexy Halladay",
    "Allie Ostrander", "Krissy Gear", "Kayley Delay", "Gracie Hyde",
    "Janette Schraft", "Colett Rampf", "Karrie Baloga", "Judi Jones",
    "Lydia Olivere", "Emma Tavella", "Madison Neuner"
])

# Women's 10000m - June 28, 2024 (straight final)
add("10K", "24", [
    "Weini Kelati", "Parker Valby", "Karissa Schweizer", "Jessica McClain",
    "Amanda Vestri", "Kellyn Taylor", "Maggie Montoya", "Erika Kemp",
    "Elly Henes", "Keira D'Amato", "Carrie Verdon", "Natosha Rogers",
    "Katie Izzo", "Susanna Sullivan", "Katrina Coogan", "Olivia Pratt",
    "Emily Lipari", "Amy Davis-Green", "Katie Camarena", "Anne-Marie Blaney",
    "Jessica Gockley-Day", "Stephanie Bruce",
    # DNF
    "Rachel Smith"
])

# ============================================================
# 2025 USATF Outdoor Championships - Eugene (July 31 - Aug 3, 2025)
# ============================================================

# Women's 10000m - July 31, 2025 (straight final)
add("10K", "25", [
    "Emily Infeld", "Elise Cranny", "Taylor Roe", "Weini Kelati",
    "Jessica McClain", "Karissa Schweizer", "Keira D'Amato", "Amanda Vestri",
    "Claire Green", "Katie Izzo", "Elly Henes", "Vanessa Fraser",
    "Katie Camarena", "Cailie Hughes", "Abby Nichols", "Sophia King",
    "Savannah Shaw", "Madison Offstein",
    # DNF
    "Rosina Machu", "Katrina Coogan", "Jessica Gockley-Day"
])

# Women's 3000m Steeplechase - Round 1 July 31, Final Aug 2
# Heat 1
add("SC", "25", [
    "Lexy Halladay-Lowry", "Val Constien", "Kaylee Mitchell", "Angelina Ellis",
    "Colett Rampf", "Logan Jolly", "Allie Ostrander", "Janette Schraft",
    "Rachel Anderson", "Sophia McDonnell", "Layla Roebke"
])
# Heat 2
add("SC", "25", [
    "Angelina Napoleon", "Gabbi Jennings", "Olivia Markezich", "Courtney Wayment",
    "Krissy Gear", "Gracie Hyde", "Emma Gee", "Calli Doan",
    "Margaret Liebich", "Emily Paupore", "Sara Van Dyke", "Grace Gilbreth"
])

# Women's 5000m - Aug 3, 2025 (straight final)
add("5K", "25", [
    "Shelby Houlihan", "Elise Cranny", "Josette Andrews", "Weini Kelati",
    "Bailey Hertenstein", "Karissa Schweizer", "Taylor Roe", "Ella Donaghu",
    "Emily Venters", "Sophia Kennedy", "Kayley DeLay", "Allie Buchalski",
    "Andrea Rodenfels", "Amaris Tyynismaa", "Alicia Monson", "Lucy Nodler Jenks",
    "Katie Camarena", "Elise Stearns", "Katelyn Tuohy", "Elena Henes",
    # DNS
    "Katie Izzo", "Emily Mackay"
])

# ============================================================
# Name normalization (handle alternates: Halladay vs Halladay-Lowry,
# Norris/Andrews same person, Gabbi/Gabrielle Jennings, Annie/Andrea Rodenfels,
# Krissy/Kristlin Gear, Elly/Elena Henes, Kelati/Kelati Frezghi, etc.)
# We use one canonical name per person.
# ============================================================
ALIASES = {
    # Josette Norris (2022) -> married name Andrews (2023+)
    "Josette Norris": "Josette Andrews",
    # Lexy Halladay (2023) -> Lexy Halladay-Lowry (2024 final actually still Lexy Halladay; 2025 listed as Halladay-Lowry)
    "Lexy Halladay": "Lexy Halladay-Lowry",
    # Annie Rodenfels (2024 final) and Andrea Rodenfels appear both — they are the same person.
    "Annie Rodenfels": "Andrea Rodenfels",
    # Kristlin Gear is the formal name for Krissy Gear
    "Kristlin Gear": "Krissy Gear",
    # Gabrielle Jennings == Gabbi Jennings
    "Gabrielle Jennings": "Gabbi Jennings",
    # Valerie Constien == Val Constien
    "Valerie Constien": "Val Constien",
    # Elena Henes is Elly Henes (different runner from Elly Henes? no — same person)
    "Elena Henes": "Elly Henes",
    # Weini Kelati Frezghi == Weini Kelati
    "Weini Kelati Frezghi": "Weini Kelati",
    # Jessica McLain (typo) -> Jessica McClain
    "Jessica McLain": "Jessica McClain",
    # Kayley DeLay == Kayley Delay
    "Kayley DeLay": "Kayley Delay",
    # Katie Thronson == Katherine Thronson
    "Katie Thronson": "Katherine Thronson",
    # Abbey Cooper - keep as is (was Abbey D'Agostino).
    # Marisa Howard - confirm consistent across years (no Howard-Sissons here).
}

# Apply aliases
canonical = []
for ev, yr, name in entries:
    name = ALIASES.get(name, name)
    canonical.append((ev, yr, name))

# Group by athlete
athletes = defaultdict(lambda: {"5K": set(), "SC": set(), "10K": set()})
for ev, yr, name in canonical:
    athletes[name][ev].add(yr)

# Build event strings
def event_str(d):
    parts = []
    for ev in ["5K", "SC", "10K"]:
        years = sorted(d[ev])
        if years:
            parts.append(f"{ev} " + " ".join(f"'{y}" for y in years))
    return ", ".join(parts)

result = []
for name in sorted(athletes.keys(), key=lambda s: s.lower()):
    result.append({
        "name": name,
        "events": event_str(athletes[name]),
        "wa_url": ""
    })

with open("/Users/trevor/Projects/CLAUDE/rr-track-research/research/usas_starters.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Total unique athletes: {len(result)}")
for a in result[:5]:
    print(a)

# Coverage summary
counts = defaultdict(int)
for ev, yr, _ in canonical:
    counts[(ev, yr)] += 1
print("\nCoverage (event-year: total entries including dupes-per-athlete-across-rounds):")
for k in sorted(counts.keys()):
    print(f"  {k[0]} '{k[1]}: {counts[k]}")
