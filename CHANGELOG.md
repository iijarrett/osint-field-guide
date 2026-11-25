# Changelog

Notable changes to the guide. Newest first. Tool-level changes (a tool added, dropped or re-rated) are recorded here;
routine review-date updates are not.

## 0.2.1, 2026-11-25

- Added `docs/METHODOLOGY.md`: how the guide's loop maps to the Berkeley Protocol's investigative cycle, a
  principle-by-principle check of the guide, the ethics and lawful-use rules, how entries are chosen and kept, and
  the guide's limits.
- Fixed the Berkeley Protocol entry: it listed seven stages with "assessment" twice. The Protocol's cycle has six.

## 0.2.0, 2026-11-24

- Added `osint-guide`, an offline command-line reader: `sections`, `list`, `search`, `show` and `install`, with
  `--os` filtering and `--json` output. It only prints; it never runs an install line or touches the network.
- Packaged with a `pyproject.toml`; the data folder is bundled into the wheel.

## 0.1.0, 2026-11-23

- First public version: 88 entries in 15 sections (a setup section, 13 sections organized by what you hold, and a
  cross-cutting tradecraft section), plus a skip list of 15 entries.
- Install lines for Windows (winget), macOS (Homebrew) and Linux (apt) wherever a tool needs installing.
- Data in `data/*.yml`; README and `docs/` generated from it; validation, tests and a weekly tool-health check in CI.
