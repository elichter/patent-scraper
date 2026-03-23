# Changelog

All notable changes to this project will be documented here.

## [1.0.0] - 2026-03-22

### Added
- Initial release
- Search patents by assignee and publication date via SerpAPI Google Patents API
- Two output sheets: **Granted** (confirmed grants only) and **All Activity** (grants + applications)
- Merges granted results into All Activity so no grants are ever missing
- Deduplicates patents with multiple titles, stacking them with ` / ` separator
- Sorts results by publication date ascending
- Full inventor list scraped from Google Patents pages (free, no API credits used)
- Inventor cache (`inventor_cache.json`) to skip re-fetching on repeat runs
- Plain-text summary file alongside Excel output
- Timestamped output directory per run
- Post-filter to remove unrelated assignees from broad SerpAPI matches
- Auto-install prompt for missing Python dependencies with version info
- Python 3.8+ version check on startup
- API credits used counter per run
- YAML-based config for API key management
- `.gitignore` excluding credentials, cache, and output directories
