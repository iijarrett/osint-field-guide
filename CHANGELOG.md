# Changelog

Notable changes to the guide. Newest first. Tool-level changes (a tool added, dropped or re-rated) are recorded here;
routine review-date updates are not.

## 0.3.0, 2026-11-25

- Added the pivot map: `data/pivots.yml` (14 kinds of thing an investigator can hold, 55 pivots between them, each
  naming the guide tools that make the hop) and `scripts/build_pivot_map.py`, which generates
  `docs/pivot-map.html` (one self-contained page, no network requests, light and dark themes, works on a phone) and
  `docs/pivot-map.json` (the same graph with tool names and links resolved, for other sites to render).
- The validator now checks the pivot data: every endpoint and tool must exist, workflow steps are not tools, and
  gated tools are rejected so the map never names the gated tier.
- CI checks that the generated pivot files are current. The page's fonts (IBM Plex Sans and JetBrains Mono, SIL Open
  Font License) are kept in `scripts/fonts/` with their licenses.

## 0.2.2, 2026-11-25

- WhatsMyName moved to the skip list: its author archived it on 9 November 2026. Blackbird's entry now says the
  dataset it reads is frozen.
- Blackbird's repository moved on GitHub from `p1ngul1n0` to `antoniaci`; links and clone line updated.
- Fixed a placeholder link in the secret-scanners entry. The validator now rejects links containing `<`, `>` or a
  space.
- Removed the SpyOnWeb link (unreachable on 25 November 2026) from the tracker-IDs entry.
- Health check: retries on HTTP 502 and 504; an optional `data/health_ignore.yml` lists accepted exceptions that
  expire after at most 180 days and appear in the report; repositories whose entry already says stale, dormant or
  slowing are no longer flagged as quiet.

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
