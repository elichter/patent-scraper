# Patent Scraper

A Python script that searches Google Patents via SerpAPI for patents by assignee, filtered from a start date through present, producing a structured Excel report with two sheets — granted patents only, and all activity (grants + applications).

## Features

- Search any assignee across all patent jurisdictions (US, WO, EP, JP, CN, and more)
- Filter by publication date — returns everything published from a start date through present
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

## Requirements

- **Python 3.8 or higher** — download at [python.org/downloads](https://www.python.org/downloads/)
- **SerpAPI key** — free at [serpapi.com](https://serpapi.com)
- Python packages are installed automatically on first run (or manually via `pip install -r requirements.txt`)

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/elichter/patent-scraper.git
   cd patent-scraper
   ```

2. **Get a SerpAPI key** — sign up free at [serpapi.com](https://serpapi.com) (250 searches/month, no credit card required). Once logged in, your API key is available at [serpapi.com/manage-api-key](https://serpapi.com/manage-api-key)

3. **Configure your key**
   ```bash
   cp config.yaml.example config.yaml
   ```
   Then open `config.yaml` and paste your key:
   ```yaml
   api_key: "your_actual_key_here"
   ```

4. **Run** — dependencies install automatically on first run
   ```bash
   python3 scrape_serpapi.py
   ```

You will be prompted for an assignee name (e.g. `Thomas Jefferson University`) and a start date (e.g. `20250101`).

## Notes

- SerpAPI's assignee filter does broad text matching. If you get unrelated results (e.g. searching "Philadelphia University" also returns Drexel results due to an acquisition), the script post-filters results to only keep patents where the returned assignee field contains your input string.
- A typical run uses 2 API credits (one for granted, one for all activity).
- `config.yaml` and any output directories are excluded from version control via `.gitignore`.
- To install dependencies manually: `pip install -r requirements.txt`

## License

MIT
