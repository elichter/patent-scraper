# Changelog

All notable changes to this project will be documented here.

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
