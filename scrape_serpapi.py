"""
Patent Scraper — SerpAPI Google Patents
Produces one Excel file with two sheets:
  1. Granted patents only
  2. All activity (grants + applications)
Plus a summary txt file.

Free tier: 250 searches/month at serpapi.com
Install: pip install requests pandas openpyxl
"""

import subprocess
import sys
import os
import time

# Python version check
if sys.version_info < (3, 8):
    sys.exit(
        f"ERROR: Python 3.8 or higher is required. "
        f"You are running Python {sys.version_info.major}.{sys.version_info.minor}. "
        f"Download the latest version at https://www.python.org/downloads/"
    )

# Auto-install missing dependencies
def install_requirements():
    pkg_map = {
        "requests":       "requests",
        "pandas":         "pandas",
        "openpyxl":       "openpyxl",
        "pyyaml":         "yaml",
        "beautifulsoup4": "bs4",
    }
    import importlib.util
    missing = [pkg for pkg, imp in pkg_map.items() if not importlib.util.find_spec(imp)]

    if not missing:
        print("All packages already installed.\n")
        return

    print("The following packages are missing and will be installed:")
    for pkg in missing:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "index", "versions", pkg],
                capture_output=True, text=True
            )
            version = "unknown"
            for line in result.stdout.splitlines():
                if "LATEST" in line:
                    version = line.split(":")[-1].strip().split(",")[0].strip()
                    break
            print(f"  {pkg} (latest: {version})")
        except Exception:
            print(f"  {pkg}")

    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    print("Done.\n")

if input("Auto-install missing packages if needed? (y/n): ").strip().lower() != "n":
    install_requirements()

import json
import yaml
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from openpyxl.styles import Font
from datetime import datetime

# Load API key from config.yaml (never commit this file — see config.yaml.example)
with open("config.yaml") as f:
    config = yaml.safe_load(f)
API_KEY = config.get("api_key", "")
if not API_KEY or API_KEY == "your_serpapi_key_here":
    raise SystemExit("ERROR: Set your SerpAPI key in config.yaml (copy from config.yaml.example)")
ASSIGNEE   = input("Enter assignee name (e.g. Thomas Jefferson University): ").strip()
AFTER_DATE = input("Enter start date for patent search (YYYYMMDD, e.g. 20250101): ").strip()
TIMESTAMP  = datetime.now().strftime('%Y%m%d_%H%M%S')
# Short tag: initials of assignee words, e.g. "Thomas Jefferson University" -> "TJU"
SHORT_TAG  = "".join(w[0].upper() for w in ASSIGNEE.split())
# Directory uses full assignee name; internal files use short tag
OUTPUT_DIR = f"search_{TIMESTAMP}_{ASSIGNEE.replace(' ', '_')}_{AFTER_DATE}"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT     = os.path.join(OUTPUT_DIR, f"{SHORT_TAG}_{AFTER_DATE}_patents.xlsx")
ENDPOINT   = "https://serpapi.com/search"

api_credits_used = 0


def fetch_all_inventors(patent_link):
    """Scrape all inventors from a Google Patents page. Free — no API credit used."""
    try:
        resp = requests.get(patent_link, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        soup = BeautifulSoup(resp.text, "html.parser")
        inventors = [tag.get_text(strip=True) for tag in soup.find_all(itemprop="inventor")]
        return ", ".join(inventors) if inventors else "N/A"
    except Exception:
        return "N/A"


CACHE_FILE = "inventor_cache.json"

def load_cache():
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def enrich_inventors(patents, label=""):
    cache = load_cache()
    print(f"\nFetching full inventor lists for {label} ({len(patents)} patents)...")
    changed = False
    for i, p in enumerate(patents):
        num = p["Patent Number"]
        if num in cache:
            p["Inventors"] = cache[num]
            print(f"  [{i+1}/{len(patents)}] {num}: {cache[num]} (cached)")
        else:
            inventors = fetch_all_inventors(p["Link"])
            p["Inventors"] = inventors
            cache[num] = inventors
            changed = True
            print(f"  [{i+1}/{len(patents)}] {num}: {inventors}")
            time.sleep(0.5)
    if changed:
        save_cache(cache)
        print(f"  Cache updated → {CACHE_FILE}")
    return patents


def fetch_page(page, status=None):
    global api_credits_used
    params = {
        "engine":   "google_patents",
        "q":        "",
        "assignee": ASSIGNEE,
        "after":    f"publication:{AFTER_DATE}",
        "num":      100,
        "page":     page,
        "api_key":  API_KEY,
    }
    if status:
        params["status"] = status
    resp = requests.get(ENDPOINT, params=params, timeout=30)
    resp.raise_for_status()
    api_credits_used += 1
    return resp.json()


def fetch_all_pages(status=None, label=""):
    patents = []
    page    = 1

    while True:
        print(f"  [{label}] Page {page}...", end=" ", flush=True)
        try:
            data = fetch_page(page, status=status)
        except Exception as e:
            print(f"Error: {e}")
            break

        if page == 1:
            info = data.get("search_information", {})
            print(f"\n  → {info.get('total_results', '?')} total results")

        results = data.get("organic_results", [])
        if not results:
            print("No results — done.")
            break

        for r in results:
            patents.append({
                "Title":            r.get("title", "N/A"),
                "Patent Number":    r.get("publication_number", "N/A"),
                "Publication Date": r.get("publication_date", "N/A"),
                "Grant Date":       r.get("grant_date", "N/A"),
                "Filing Date":      r.get("filing_date", "N/A"),
                "Priority Date":    r.get("priority_date", "N/A"),
                "Inventors":        r.get("inventor", "N/A"),
                "Assignee":         r.get("assignee", "N/A"),
                "Abstract":         r.get("snippet", "N/A"),
                "Link":             r.get("patent_link", "N/A"),
            })

        print(f"got {len(results)} (total: {len(patents)})")

        if not data.get("serpapi_pagination", {}).get("next"):
            print("  Done.")
            break

        page += 1
        time.sleep(1)

    return patents


def prepare_df(patents):
    df = pd.DataFrame(patents)
    df = df.groupby("Patent Number", as_index=False).agg({
        "Title": lambda x: " / ".join(x.unique()),
        **{col: "first" for col in df.columns if col not in ["Patent Number", "Title"]}
    })
    df = df.sort_values("Publication Date", ascending=True)
    return df


def save_excel(df_granted, df_all, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df_granted.to_excel(writer, sheet_name="Granted", index=False)
        df_all.to_excel(writer, sheet_name="All Activity", index=False)

    wb = openpyxl.load_workbook(path)
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        for cell in ws[1]:
            cell.font = Font(bold=True)
    wb.save(path)
    print(f"\n✓ Saved to {path}")
    print(f"  Sheet 'Granted': {len(df_granted)} patents")
    print(f"  Sheet 'All Activity': {len(df_all)} patents")


def save_summary(df_granted, df_all, granted_raw, all_raw, path):
    originally_missing = {
        p["Patent Number"] for p in granted_raw
        if p["Patent Number"] not in {x["Patent Number"] for x in all_raw}
    }
    granted_dupes = df_granted[df_granted["Title"].str.contains(" / ", na=False)]
    all_dupes     = df_all[df_all["Title"].str.contains(" / ", na=False)]

    with open(path, "w") as f:
        f.write(f"Patent Search Summary\n")
        f.write(f"Assignee: {ASSIGNEE}\n")
        f.write(f"After: {AFTER_DATE}\n")
        f.write(f"Generated: {TIMESTAMP}\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"GRANTED ({len(df_granted)} patents):\n")
        for _, row in df_granted.iterrows():
            f.write(f"  {row['Patent Number']} | {row.get('Grant Date','N/A')} | {row['Title'][:80]}\n")

        f.write(f"\nALL ACTIVITY ({len(df_all)} patents):\n")
        for _, row in df_all.iterrows():
            status = "Granted" if pd.notna(row.get("Grant Date")) and str(row.get("Grant Date")) not in ("NaT", "nan", "N/A", "") else "Application"
            f.write(f"  [{status}] {row['Patent Number']} | {row.get('Publication Date','N/A')} | {row['Title'][:80]}\n")

        f.write(f"\nDUPLICATE TITLES IN GRANTED ({len(granted_dupes)}):\n")
        for _, row in granted_dupes.iterrows():
            f.write(f"  {row['Patent Number']} | {row['Title']}\n")
        if len(granted_dupes) == 0:
            f.write("  None\n")

        f.write(f"\nDUPLICATE TITLES IN ALL ACTIVITY ({len(all_dupes)}):\n")
        for _, row in all_dupes.iterrows():
            f.write(f"  {row['Patent Number']} | {row['Title']}\n")
        if len(all_dupes) == 0:
            f.write("  None\n")

        f.write(f"\nADDED TO ALL ACTIVITY FROM GRANTED ({len(originally_missing)}):\n")
        if originally_missing:
            for num in sorted(originally_missing):
                row = df_granted[df_granted["Patent Number"] == num].iloc[0]
                f.write(f"  {num} | {row.get('Grant Date','N/A')} | {row['Title'][:80]}\n")
        else:
            f.write("  None\n")

    print(f"✓ Summary written to {path}")


def scrape():
    print(f"\n=== SerpAPI Google Patents ===")
    print(f"Assignee: '{ASSIGNEE}', after {AFTER_DATE}\n")

    print("--- Query 1: Granted patents ---")
    granted = fetch_all_pages(status="GRANT", label="GRANT")

    print()

    print("--- Query 2: All activity ---")
    all_patents = fetch_all_pages(status=None, label="ALL")

    if granted or all_patents:
        df_granted = prepare_df(granted) if granted else pd.DataFrame()

        merged = all_patents.copy()
        all_numbers = {p["Patent Number"] for p in merged}
        for p in granted:
            if p["Patent Number"] not in all_numbers:
                merged.append(p)

        df_all = prepare_df(merged) if merged else pd.DataFrame()

        save_excel(df_granted, df_all, OUTPUT)
        summary_path = os.path.join(OUTPUT_DIR, f"{SHORT_TAG}_{AFTER_DATE}_summary.txt")
        save_summary(df_granted, df_all, granted, all_patents, summary_path)

    print(f"\nAPI credits used this run: {api_credits_used}")
    print(f"Check live balance at: https://serpapi.com/dashboard")


if __name__ == "__main__":
    scrape()
