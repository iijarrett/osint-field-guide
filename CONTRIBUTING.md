# Contributing

Thanks for helping keep this list accurate. OSINT sources die faster than almost any other kind, so corrections
matter more than additions.

## Quick ways to help

- **A link is dead or a tool changed.** Open a *Dead link or changed tool* issue, or fix it in a pull request.
- **A tool is missing.** Open a *Suggest a tool* issue. The bar below decides whether it goes in.
- **An install line failed on your OS.** Open an issue with your OS version and the error. winget IDs and apt package
  names are the least-checked part of the data, so these reports are especially useful.

## The inclusion bar

An entry earns its place if it passes all of these.

1. **It is the best option for a specific job**, or a genuine second pick that finds something the first one misses.
   Say what the job is and why this tool wins. "Also exists" is not a reason.
2. **It is maintained, or its status is stated.** Dormant tools can stay if they are still the best and the entry says
   so plainly (`status` in the *kind* line and a sentence in `why`). Dead tools go on the skip list with the reason.
3. **Claims carry a date.** Prices, free-tier limits, versions and ownership change. Put the month in the text
   ("as of November 2026") and update `verified.date`.
4. **Installation is inspectable.** Use pipx, uv, `go install`, `git clone`, Docker, Homebrew, winget or apt. No
   `curl | bash` or `iwr | iex`. If upstream only offers one, link to it and describe the alternative in a note.
5. **The ethics are in the entry.** A tool that can be used to harm a person (face search, breach records, people
   search, anything that touches accounts) is tagged `gated`, gets a `caution`, and leads with the lawful, defensive
   use. A tool whose main use is stalking, doxxing, credential abuse or access to systems you are not authorized to
   test will not be accepted.
6. **No affiliate links, sponsored placement or tracking links.**

## Handling a tool-health report

The weekly health issue lists what needs a person. For each finding, check it by hand, then either fix the data
(move a renamed repository, update a changed link, move a dead tool to `data/skip.yml`) or, if the finding is a
false alarm you have confirmed, add the URL to `data/health_ignore.yml` with a reason and an expiry date.

## How to edit the data

The README and every numbered page under `docs/` are generated. Do not edit them by hand.
`docs/METHODOLOGY.md` is the exception: it is written by hand.

```sh
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
# edit data/tools.yml (or sections.yml, skip.yml)
python scripts/build_readme.py                        # regenerate README.md and docs/
python scripts/build_pivot_map.py                     # regenerate docs/pivot-map.html and .json
python scripts/build_tools_json.py                    # regenerate docs/tools.json
python scripts/validate.py                            # schema and rule checks
python -m pytest -q                                   # data, build, health-check and command-line tests
python -m pytest -q                                   # includes "generated files are current"
```

A new entry in `data/tools.yml` looks like this:

```yaml
- id: exampletool                 # lowercase slug, unique
  name: ExampleTool
  section: 05-domain-ip-network   # an id from data/sections.yml
  kind: free · local tool · Go    # cost · type · language or status
  tier: deeper                    # start | deeper | gated
  summary: One line, under about 110 characters.
  what: What it does, in a few sentences.
  why: "*Why this one:* what it finds that the others miss, and its limits."
  install:
    - {os: All OS, cmd: go install example.com/cmd/exampletool@latest}
    - {os: Run, cmd: exampletool -d example.com}
  links:
    - {label: example.com, url: https://example.com/}
  github: owner/repo              # optional; the weekly check watches it
  caution:                        # required for gated tools
    title: Short bold lead-in
    body: What can go wrong and what the lawful use is.
  verified: {date: "2026-11-23", install_checked: partial}
```

`install_checked` is `yes` only if you ran every line on every OS you list; otherwise use `partial`. Write section
cross-references as `§05`; the build turns them into links.

## Pull requests

- One topic per pull request, with a sentence on why.
- CI must pass: validation, tests and "generated files are up to date".
- Keep commit messages plain and descriptive.

## Conduct

Be kind and be precise. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Report security problems as described in
[SECURITY.md](SECURITY.md), not in public issues.
