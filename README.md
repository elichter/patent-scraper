# Patent Scraper

A Python script that searches Google Patents via SerpAPI for patents by **assignee and date range**, producing a structured Excel report with two sheets — granted patents only, and all activity (grants + applications).

## Features

- Search any assignee across all patent jurisdictions (US, WO, EP, JP, CN, and more)
- Filter by publication date — returns everything published after a date you specify
- Two output sheets: **Granted** (confirmed grants only) and **All Activity** (grants + applications)
- Merges results from both queries so no grants are ever missing from All Activity
- Deduplicates patents with multiple titles (stacks them in one cell separated by ` / `)
- Sorts by publication date ascending
- Generates a plain-text summary file alongside the Excel
- Organized output: each run creates its own timestamped directory
- Tracks API credits used per run
- Auto-installs missing Python dependencies on first run

## Output

Each run creates a directory like:
```
search_20260101_120000_Thomas_Jefferson_University_20250101/
├── TJU_20250101_patents.xlsx      # Excel with Granted + All Activity sheets
└── TJU_20250101_summary.txt       # Plain text summary
```

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/elichter/patent-scraper.git
cd patent-scraper

# 2. Set up your API key
cp config.yaml.example config.yaml
# Edit config.yaml and paste your SerpAPI key

# 3. Run — dependencies install automatically on first run
python3 scrape_serpapi.py
```

You will be prompted for:
- **Assignee name** — e.g. `Thomas Jefferson University`
- **Start date** — e.g. `20250101` (YYYYMMDD format)

## Setup

### SerpAPI Key
1. Sign up for a free account at [serpapi.com](https://serpapi.com) — 250 free searches/month, no credit card required
2. Copy `config.yaml.example` to `config.yaml`
3. Paste your key:

```yaml
api_key: "your_actual_key_here"
```

`config.yaml` is listed in `.gitignore` and will never be committed to GitHub.

### Dependencies
Dependencies are checked and installed automatically when you run the script. To install manually:

```bash
pip install -r requirements.txt
```

## Notes

- SerpAPI's assignee filter does broad text matching. If you get unrelated results (e.g. searching "Philadelphia University" also returns Drexel results due to an acquisition), the script post-filters results to only keep patents where the returned assignee field contains your input string.
- A typical run uses 2 API credits (one for granted, one for all activity).
- `config.yaml` and any output directories are excluded from version control via `.gitignore`.

## License

MIT
