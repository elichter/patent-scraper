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
   nano config.yaml
   ```
   Replace `your_serpapi_key_here` with your actual key, then save with `Ctrl+O`, `Enter`, `Ctrl+X`.

4. **Run**
   ```bash
   python3 scrape_serpapi.py
   ```

   You will be prompted for:
   - **Auto-install missing packages? (y/n)** — enter `y` to have the script check for and install any missing dependencies automatically. Enter `n` if you prefer to manage dependencies yourself — note that the script will error if any required packages are missing.
   - **Assignee name** — e.g. `Thomas Jefferson University`
   - **Start date** — e.g. `20250101` (YYYYMMDD format)
   - **Parallel fetch? (y/n)** — enter `y` for faster inventor/co-assignee scraping using parallel requests, or `n` for sequential (safer, less likely to be rate-limited). If `y`, you will also be asked how many parallel workers to use (recommended: 3-10, default 5)
   - **Assignee review** — after fetching, the script displays all unique assignee names returned by SerpAPI and asks you to exclude any that do not match your institution (useful for ambiguous names like "Philadelphia University" which may return results from other Philadelphia-based institutions)

## Notes

- SerpAPI's assignee filter does broad text matching. The interactive assignee review step lets you exclude any false positives before saving.
- A typical run uses 2 API credits (one for granted, one for all activity).
- Inventor and co-assignee data is cached locally in `patent_cache.json` — repeat runs skip HTTP requests for patents already seen, making subsequent runs faster. The cache is shared across searches so running multiple institutions on the same device will reuse cached data.
- `config.yaml`, `patent_cache.json`, and any output directories are excluded from version control via `.gitignore`.
- To install dependencies manually: `pip install -r requirements.txt`
- **conda users who prefer not to mix pip:** run `conda install requests pandas openpyxl pyyaml beautifulsoup4` before running the script, then answer `n` when prompted about auto-installing packages.

## License

MIT
