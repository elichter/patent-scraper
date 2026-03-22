# Patent Scraper

A Python script that searches Google Patents via SerpAPI for patents by assignee, producing a structured Excel report with two sheets — granted patents and all activity.

## Features

- Search any assignee across all patent jurisdictions (US, WO, EP, JP, etc.)
- Two output sheets: **Granted** (confirmed grants only) and **All Activity** (grants + applications)
- Merges results from both queries so no grants are missed
- Deduplicates patents with multiple titles (stacks them in one cell)
- Sorts by publication date ascending
- Generates a plain-text summary file alongside the Excel
- Organized output: each run creates its own timestamped directory
- Tracks API credits used per run

## Output

Each run creates a directory like:
```
search_20260101_120000_Thomas_Jefferson_University_20250101/
├── TJU_20250101_patents.xlsx      # Excel with Granted + All Activity sheets
└── TJU_20250101_summary.txt       # Plain text summary
```

## Requirements

```bash
pip install requests pandas openpyxl pyyaml
```

## Setup

1. Sign up for a free SerpAPI account at [serpapi.com](https://serpapi.com) (250 free searches/month)
2. Copy `config.yaml.example` to `config.yaml`
3. Paste your SerpAPI key into `config.yaml`

```yaml
api_key: "your_actual_key_here"
```

## Usage

```bash
python3 scrape_serpapi.py
```

You will be prompted for:
- **Assignee name** — e.g. `Thomas Jefferson University`
- **Start date** — e.g. `20250101` (YYYYMMDD format)

## Notes

- The `assignee` filter in SerpAPI does broad text matching. If you get unrelated results, the script includes a post-filter that keeps only patents where the returned assignee field contains your input string.
- SerpAPI free tier allows 250 searches/month. A typical run uses 2 searches.
- `config.yaml` is excluded from version control via `.gitignore`.

## License

MIT
