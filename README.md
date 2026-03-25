# Patent Scraper → Patent Intelligence Pipeline

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/elichter/patent-scraper)
![Stars](https://img.shields.io/github/stars/elichter/patent-scraper?style=social)

> **Keywords:** patent search · patent analytics · Google Patents · patent scraper · tech transfer · IP intelligence · intellectual property · patent data Python · assignee search · patent landscape

A Python-based pipeline for **patent search, retrieval, and structuring** across all major patent jurisdictions (US, WO, EP, JP, CN, and more). Built for tech transfer professionals, IP attorneys, researchers, and analysts who need structured, analysis-ready patent data without manual searching.

Enables downstream workflows including **patent landscape analysis**, **competitive intelligence**, **prior art research**, and **technology trend detection** — all from a single command-line tool.

---

## Overview

Patent data is large-scale, semi-structured, and difficult to work with directly.  
This project automates:

- Retrieval of patent records across jurisdictions
- Parsing and normalization of metadata (assignees, inventors, dates)
- Deduplication and consolidation of records
- Export into analysis-ready structured formats

The output is designed for immediate use in Excel, data science workflows, or strategic analysis.

---

## Key Features

- Search any assignee across global patent systems (US, WO, EP, JP, CN, etc.)
- Filter by publication date (from a specified start date through present, or a specific date range)
- Dual dataset output:
  - **Granted patents only**
  - **All activity (grants + applications)**
- Ensures completeness by merging queries so no granted patents are missed
- Deduplicates patents with multiple titles (merged into a single record)
- Built-in assignee review step ensures accuracy by letting users validate results before saving
- Tracks API credit usage per run
- Caches inventor and co-assignee data for efficiency across runs
- Parallelized data retrieval (optional) for faster execution
- Auto-installs missing Python dependencies on first run

---

## Example Output

Each run produces a structured Excel file and summary:

```
search_20260101_120000_Thomas_Jefferson_University_20250101/
├── TJU_20250101_patents.xlsx
└── TJU_20250101_summary.txt
```

### Sample Record (for illustrative purposes)

| Patent Number | Title | Assignee | Co-Assignees | Publication Date | Grant Date |
|--------------|-------|----------|--------------|------------------|------------|
| US12269155B2 | Multivalent vaccines for rabies virus and coronaviruses | Thomas Jefferson University | University of Maryland Baltimore, US Department of Health and Human Services | 2025-04-08 | 2025-04-08 |
| AU2022206776B2 | Methods and compositions for treating cancers | Thomas Jefferson University | None | 2025-05-08 | 2025-05-08 |

---

## Why This Matters

Structured patent data enables:

- Identification of emerging technology trends
- Competitive intelligence on company R&D pipelines
- Prior art and landscape analysis
- Supporting IP strategy, licensing decisions, and technology landscape analysis across all industries

---

## Technical Design

Pipeline overview:

```
SerpAPI → Retrieval Layer → Parsing & Normalization → Deduplication → Structured Output (Excel)
```

Key components:
- API querying (SerpAPI / Google Patents)
- HTML parsing (BeautifulSoup)
- Data structuring (pandas)
- Local caching for performance optimization

---

## Getting Started

### Requirements

- **Python 3.8 or higher** — download at [python.org/downloads](https://www.python.org/downloads/)
- **SerpAPI key** — free at [serpapi.com](https://serpapi.com) (250 searches/month, no credit card required). Once logged in, your API key is available at [serpapi.com/manage-api-key](https://serpapi.com/manage-api-key)
- Python packages are installed automatically on first run (or manually via `pip install -r requirements.txt`)

### Setup

```bash
git clone https://github.com/elichter/patent-scraper.git
cd patent-scraper
cp config.yaml.example config.yaml
nano config.yaml
```

Replace `your_serpapi_key_here` with your actual key, then save with `Ctrl+O`, `Enter`, `Ctrl+X`.

### Run

```bash
python3 scrape_serpapi.py
```

You will be prompted for:
- **Auto-install missing packages? (y/n)** — enter `y` to have the script check for and install any missing dependencies automatically. Enter `n` if you prefer to manage dependencies yourself — note that the script will error if any required packages are missing.
- **Assignee name** — e.g. `Thomas Jefferson University`
- **Date filter** — choose between a start date through present (e.g. `20250101`) or a specific date range (e.g. `20230101` to `20251231`)
- **Parallel fetch? (y/n)** — enter `y` for faster inventor/co-assignee scraping using parallel requests, or `n` for sequential (safer, less likely to be rate-limited). If `y`, you will also be asked how many parallel workers to use (recommended: 3-10, default 5)
- **Assignee review** — after fetching, the script displays all unique assignee names returned by SerpAPI and asks you to exclude any that do not match your institution. A 30-second countdown timer auto-proceeds with all assignees if left unattended (useful for scheduled or unattended runs)

---

## Notes

- Typical run uses ~2 API credits (one for granted, one for all activity)
- Inventor and co-assignee data is cached locally in `patent_cache.json` — repeat runs skip HTTP requests for patents already seen, making subsequent runs faster. The cache is shared across searches so running multiple institutions on the same device will reuse cached data
- `config.yaml`, `patent_cache.json`, and any output directories are excluded from version control via `.gitignore`
- To install dependencies manually: `pip install -r requirements.txt` (includes `requests`, `pandas`, `openpyxl`, `pyyaml`, `beautifulsoup4`, `matplotlib`, `scikit-learn`, `wordcloud`)
- **conda users who prefer not to mix pip:** run `conda install requests pandas openpyxl pyyaml beautifulsoup4 matplotlib scikit-learn && pip install wordcloud` before running the script, then answer `n` when prompted about auto-installing packages

---

## Examples

![Grants by Year](grants_by_year.png)

*Sample output: granted patents by year for Thomas Jefferson University (illustrative data)*

See [EXAMPLES.md](EXAMPLES.md) for practical walkthroughs including:
- University tech transfer searches (Thomas Jefferson University)
- Handling ambiguous assignee names (Philadelphia University)
- Large corporate assignees with international filings
- Downstream analysis and visualization: grants by year, co-assignees, jurisdiction activity, word cloud, technology clustering (t-SNE), and semantic similarity search
- Monitoring a patent portfolio over time with incremental runs

---

## Known Limitations

- **Non-US jurisdiction data gaps** — Google Patents does not always index grant dates, priority dates, or co-assignee information for non-US patents (e.g. NZ, AU, some EP filings). These fields may appear as N/A even when the patent is granted.
- **SerpAPI broad matching** — the assignee filter may return patents from similarly named institutions. The interactive assignee review step mitigates this but manual verification is recommended for ambiguous names.
- **Data currency** — SerpAPI reflects Google Patents data which may lag official patent office records by days to weeks.
- **Rate limiting** — parallel fetching may trigger rate limiting from Google Patents. Reduce worker count or switch to sequential mode if you encounter errors.

---

## License

MIT
