# Changelog

All notable changes to this project will be documented here.

## [1.2.0] - 2026-03-25

### Added
- Co-assignee scraping from Google Patents "Current Assignee" section (free — no API credits)
- Full inventor list scraped from Google Patents pages (free — no API credits)
- Both inventors and co-assignees fetched in a single HTTP request per patent
- Patent cache (`patent_cache.json`) stores inventors and co-assignees — repeat runs skip re-fetching
- Optional parallel fetching via `ThreadPoolExecutor` with user-configurable worker count
- Interactive assignee review step — displays all unique assignee names and lets user exclude false positives
- 30-second countdown timer on assignee review — auto-proceeds if left unattended
- Date range option — choose between start date through present, or a specific date range
- Excluded institutions logged in summary txt with patent numbers and titles per institution
- Monthly API credit tracker (`usage_tracker.json`) — tracks usage per month, auto-resets, warns at <20 remaining
- Configurable monthly credit limit in `config.yaml` (default 250 for free tier)
- Co-Assignees column added to Excel output, positioned after Assignee column
- Explicit column order enforced in output
- `images/` folder for all chart assets
- `EXAMPLES.md` with 5 practical examples including real sample outputs
- Visualization examples: grants by year, top co-assignees, jurisdiction activity, word cloud, t-SNE clustering, semantic similarity search
- `wordcloud_TJU.png`, `patent_clustering.png`, `patent_similarity.png` sample chart images
- `scikit-learn` and `wordcloud` added to dependencies
- GitHub topics, marketing README with badges and SEO keywords
- Known Limitations section in README
- Deep links from README to EXAMPLES.md sections

### Changed
- Post-filter replaced by interactive assignee review (handles non-English assignee names correctly)
- `inventor_cache.json` replaced by `patent_cache.json` (stores both inventors and co-assignees)
- Output directory uses full assignee name; internal files use short tag (e.g. `TJU_`)
- README fully redesigned with marketing copy, pipeline overview, and sample record table
- Co-Assignees `NaN` normalized to string `"None"` consistently throughout

### Fixed
- Non-US patents (JP, KR, etc.) no longer incorrectly filtered out by English-only assignee matching
- Duplicate README sections removed
- Co-assignee filter now handles both `"None"` string and `NaN` values

## [1.1.0] - 2026-03-23

### Added
- Full inventor list scraped from Google Patents pages (free, no API credits used)
- Co-assignee scraping from Google Patents "Current Assignee" section
- Both inventors and co-assignees fetched in a single HTTP request per patent
- Patent cache (`patent_cache.json`) stores inventors and co-assignees — repeat runs skip re-fetching
- Cache is shared across searches so multiple institution searches reuse cached data
- Optional parallel fetching via `ThreadPoolExecutor` for faster enrichment
- User-configurable number of parallel workers (default 5)
- Interactive assignee review step — displays all unique assignee names returned by SerpAPI and lets user exclude false positives before saving
- Co-Assignees column added to Excel output, positioned after Assignee column
- Explicit column order enforced in output: Title, Patent Number, Dates, Inventors, Assignee, Co-Assignees, Abstract, Link

### Changed
- Post-filter replaced by interactive assignee review (more accurate, handles non-English assignee names)
- `inventor_cache.json` replaced by `patent_cache.json` (stores both inventors and co-assignees)

## [1.0.0] - 2026-03-22

### Added
- Initial release
- Search patents by assignee and publication date via SerpAPI Google Patents API
- Two output sheets: **Granted** (confirmed grants only) and **All Activity** (grants + applications)
- Merges granted results into All Activity so no grants are ever missing
- Deduplicates patents with multiple titles, stacking them with ` / ` separator
- Sorts results by publication date ascending
- Plain-text summary file alongside Excel output
- Timestamped output directory per run
- Auto-install prompt for missing Python dependencies with version info
- Python 3.8+ version check on startup
- API credits used counter per run
- YAML-based config for API key management
- `.gitignore` excluding credentials, cache, and output directories
