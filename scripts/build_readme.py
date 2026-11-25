#!/usr/bin/env python3
"""Generate README.md and docs/*.md from data/*.yml.

    python scripts/build_readme.py          write the files
    python scripts/build_readme.py --check  exit 1 if any generated file is out of date
"""
import re
import sys
from pathlib import Path

from osintlib import ASSUMES, ROOT, TIERS, load, real_tools, validate

OWNER_REPO = "iijarrett/osint-field-guide"
BANNER = "<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->\n"
TIER_BADGE = {"start": "`START`", "deeper": "`DEEPER`", "gated": "`GATED`"}

# Sections whose title starts with "You ..." are the selector sections shown in the finder table.
SELECTOR_RANKS = [f"{i:02d}" for i in range(1, 14)]

SKIP_SLUG = "15-skip"


def esc_cell(t):
    return t.replace("|", "\\|").replace("\n", " ")


def link_refs(text, sections, base):
    """Turn section references like §05 into links to the matching docs page."""
    by_rank = {s["rank"]: s["id"] for s in sections}

    def sub(m):
        rank = m.group(1)
        if rank in by_rank:
            return "[§%s](%s%s.md)" % (rank, base, by_rank[rank])
        return m.group(0)

    return re.sub(r"§(\d\d)(?![\d])", sub, text)


def install_block(rows):
    lines = []
    prev = None
    for r in rows:
        label, cmd, note = r.get("os", ""), r.get("cmd"), r.get("note")
        if cmd:
            if label and label != prev:
                lines.append("# %s" % label)
            lines.append(cmd)
            if note:
                lines.append("#   %s" % note)
            prev = label or prev
        else:
            lines.append("# %s: %s" % (label, note) if label else "# %s" % note)
            prev = label or prev
    return "```sh\n" + "\n".join(lines) + "\n```"


def render_tool(t, sections):
    out = []
    out.append('<a id="%s"></a>' % t["id"])
    out.append("### %s" % t["name"])
    meta = []
    if t.get("tier"):
        meta.append(TIER_BADGE[t["tier"]])
    meta.append(t["kind"])
    out.append(" · ".join(meta))
    out.append("")
    out.append(link_refs(t["what"], sections, ""))
    if t.get("why"):
        out.append("")
        out.append(link_refs(t["why"], sections, ""))
    if t.get("install"):
        out.append("")
        out.append("**Install and run**")
        out.append("")
        out.append(install_block(t["install"]))
    for n in t.get("notes", []) or []:
        out.append("")
        out.append(link_refs(n, sections, ""))
    body = " ".join([t.get("what", ""), t.get("why", "")] + list(t.get("notes", []) or []))
    extra = [l for l in t.get("links", []) or [] if "](%s)" % l["url"] not in body]
    if extra:
        out.append("")
        out.append("**Links:** " + " · ".join("[%s](%s)" % (l["label"], l["url"]) for l in extra))
    if t.get("caution"):
        c = t["caution"]
        out.append("")
        head = "**%s.** " % c["title"].rstrip(".") if c.get("title") else ""
        out.append("> %s%s" % (head, link_refs(c.get("body", ""), sections, "")))
    v = t.get("verified")
    if v:
        chk = {"yes": "install lines checked", "partial": "install lines partly checked (see section 00)", "no": "install lines not checked"}.get(
            v.get("install_checked"), "")
        out.append("")
        out.append("<sub>Last reviewed %s%s</sub>" % (v["date"], " · " + chk if chk else ""))
    return "\n".join(out)


def render_section_page(sec, tools, sections, prev_s, next_s):
    out = [BANNER]
    nav = []
    if prev_s:
        nav.append("[← %s](%s.md)" % (prev_s["title"], prev_s["id"]))
    nav.append("[Index](../README.md)")
    if next_s:
        nav.append("[%s →](%s.md)" % (next_s["title"], next_s["id"]))
    out.append(" · ".join(nav) + "\n")
    out.append("# %s. %s\n" % (sec["rank"], sec["title"]))
    if sec.get("intro"):
        out.append(link_refs(sec["intro"], sections, "") + "\n")
    items = [t for t in tools if t["section"] == sec["id"]]
    if any(not t.get("step") for t in items):
        out.append("| Tool | Tier | Cost and kind |")
        out.append("|---|---|---|")
        for t in items:
            out.append("| [%s](#%s) | %s | %s |" % (esc_cell(t["name"]), t["id"], TIER_BADGE.get(t.get("tier"), ""), esc_cell(t["kind"])))
        out.append("")
    for t in items:
        out.append(render_tool(t, sections))
        out.append("")
        out.append("---\n")
    out.append("[← Back to the index](../README.md)\n")
    return "\n".join(out)


def render_skip_page(sec, skips, sections, prev_s):
    out = [BANNER]
    nav = []
    if prev_s:
        nav.append("[← %s](%s.md)" % (prev_s["title"], prev_s["id"]))
    nav.append("[Index](../README.md)")
    out.append(" · ".join(nav) + "\n")
    out.append("# %s. %s\n" % (sec["rank"], sec["title"]))
    if sec.get("intro"):
        out.append(link_refs(sec["intro"], sections, "") + "\n")
    for s in skips:
        out.append("**%s**\n" % s["name"])
        out.append(link_refs(s["why"], sections, "") + "\n")
    out.append("[← Back to the index](../README.md)\n")
    return "\n".join(out)


def first_clause(t, limit=150):
    if len(t) <= limit:
        return t
    return t[:limit].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"


def render_readme(sections, tools, skips):
    rt = real_tools(tools)
    n_tools = len(rt)
    n_gated = sum(1 for t in rt if t.get("tier") == "gated")
    n_start = sum(1 for t in rt if t.get("tier") == "start")
    out = [BANNER]
    out.append("# OSINT Field Guide\n")
    out.append(
        "[![Validate](https://github.com/%s/actions/workflows/validate.yml/badge.svg)](https://github.com/%s/actions/workflows/validate.yml) "
        "[![Tool health](https://github.com/%s/actions/workflows/health.yml/badge.svg)](https://github.com/%s/actions/workflows/health.yml) "
        "[![Code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE) "
        "[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%%20BY%%204.0-lightgrey)](LICENSE-CONTENT.md)\n"
        % ((OWNER_REPO,) * 4))
    out.append(
        "**A short list of the best open-source-intelligence tools, organized by what you have in your hand: "
        "a username, an email, a photo, a domain, a wallet.** %d entries, with install lines for Windows, macOS and Linux wherever there is something to install, "
        "plain notes on each tool's limits, and a weekly health check that flags dead links and abandoned projects.\n" % n_tools)
    out.append("## Why this one is different\n")
    out.append(
        "- **Start from the selector, not the tool.** OSINT is pivoting: one identifier leads to the next. "
        "Find the thing you hold in the table below and work that section; each section ends where another begins.\n"
        "- **A shortlist, not a directory.** Where one tool is clearly the best for the job it is listed alone. "
        "A second tool earns a place only when it finds something the first one misses. There is also a "
        "[skip list](docs/%s.md) of tools that are still recommended elsewhere but are dead, broken or a bad idea.\n"
        "- **Install lines for three operating systems.** pipx, uv, `go install`, `git clone`, Docker, Homebrew, winget and apt. "
        "No piped-to-shell installers; every line is something you can read before you run it.\n"
        "- **Honest about status.** Each entry carries a review date and says how far its install lines were checked. "
        "A scheduled workflow checks every link and every GitHub repository, and opens an issue when something dies, "
        "moves or goes quiet for a year.\n"
        "- **Ethics are part of the entry.** Tools that can hurt people are tagged `GATED`, explained with the legal exposure, "
        "and shown with their defensive use. This is a guide for investigators and defenders, not for stalkers.\n" % SKIP_SLUG)
    out.append("## Find your starting point\n")
    out.append("| You have | Go to | Tools |")
    out.append("|---|---|---|")
    by_sec = {}
    for t in rt:
        by_sec.setdefault(t["section"], []).append(t)
    for s in sections:
        if s["rank"] in SELECTOR_RANKS:
            out.append("| %s | [Section %s](docs/%s.md) | %d |" % (s["title"][:1].lower() + s["title"][1:] if False else s["title"], s["rank"], s["id"], len(by_sec.get(s["id"], []))))
    for s in sections:
        if s["rank"] == "14":
            out.append("| **Cross-cutting:** tradecraft, capture and analysis | [Section %s](docs/%s.md) | %d |" % (s["rank"], s["id"], len(by_sec.get(s["id"], []))))
        if s["rank"] == "00":
            pass
    out.append("")
    s00 = next(s for s in sections if s["rank"] == "00")
    out.append(
        "**New to this?** Read [Section 00: %s](docs/%s.md) first. It covers the research machine, the case folder and the "
        "seven-step loop every investigation follows. %s\n" % (s00["title"], s00["id"], ASSUMES))
    out.append("## How to read an entry\n")
    out.append(
        "| Tag | Meaning |\n|---|---|\n"
        "| `START` | Free, fast, no setup worth mentioning. The first thing to reach for in that section (%d tools). |\n"
        "| `DEEPER` | More setup: an install, API keys, a free account or patience. Where the real results usually are. |\n"
        "| `GATED` | Costs money, needs a business email, or carries real ethical or legal weight (%d tools). Know it exists; think before you reach. |\n"
        % (n_start, n_gated))
    out.append(
        "The *kind* line under each name says whether something is a site (nothing to install), a local tool, or paid. "
        "Most OSINT is websites, so most entries have nothing to install.\n")
    out.append(
        "**Method and ethics.** How the guide's loop lines up with the Berkeley Protocol, where it is thin, and what is "
        "gated and why: [docs/METHODOLOGY.md](docs/METHODOLOGY.md).\n")
    out.append("## Read it from the terminal\n")
    out.append(
        "The same data is available offline as a small command-line reader. It prints entries, cautions and the install lines for "
        "your OS, and **never runs anything**.\n\n"
        "```sh\n"
        "pipx install git+https://github.com/%s     # or: pip install .  from a clone\n"
        "osint-guide search username                    # find entries by word\n"
        "osint-guide show maigret                       # the full entry, with your OS's install lines\n"
        "osint-guide install maigret --os macos         # just the commands, ready to copy\n"
        "osint-guide list --tier gated                  # the entries that carry a caution\n"
        "```\n\n"
        "Add `--json` to any command to pipe the result into your own tools.\n" % OWNER_REPO)
    out.append("## The guide\n")
    for s in sections:
        if s["rank"] == SKIP_SLUG[:2]:
            continue
        items = by_sec.get(s["id"], [])
        if not items:
            continue
        out.append("### %s. [%s](docs/%s.md)\n" % (s["rank"], s["title"], s["id"]))
        out.append("| Tool | Tier | What it is for |")
        out.append("|---|---|---|")
        for t in items:
            out.append("| [%s](docs/%s.md#%s) | %s | %s |" % (esc_cell(t["name"]), s["id"], t["id"], TIER_BADGE.get(t.get("tier"), ""), esc_cell(first_clause(t["summary"]))))
        out.append("")
    skip_sec = next(s for s in sections if s["id"] == SKIP_SLUG)
    out.append("### %s. [%s](docs/%s.md)\n" % (skip_sec["rank"], skip_sec["title"], skip_sec["id"]))
    out.append("%d tools and habits that keep getting recommended and shouldn't be. Each has the reason.\n" % len(skips))
    out.append("## Ground rules\n")
    out.append(
        "1. **Pivot deliberately.** Each finding is a new selector. The skill is seeing which thread to pull, and stopping when it stops paying.\n"
        "2. **Corroborate before you conclude.** One aggregator hit is a rumor; a hit confirmed against a primary record is a finding. Keep those two words apart in your notes.\n"
        "3. **Capture at the moment of discovery.** URL, UTC timestamp, screenshot, archive link. Pages vanish, and the interesting ones vanish fastest.\n"
        "4. **Know whether you are passive or active.** Reading a certificate log touches nobody. Brute-forcing subdomains or joining a server does. "
        "The distinction governs your scope, your legal position and whether the target knows you are there.\n")
    out.append(
        "**Law and ethics.** Every source in this guide is public, and looking at public information is lawful nearly everywhere. "
        "What changes that is who you point it at and what you do next: active reconnaissance without authorization can be unauthorized access; "
        "compiling a profile on a private individual without a lawful basis can be harassment or a data-protection offence; and using a credential "
        "you found, however you found it, is a crime in essentially every jurisdiction. Professionally the rule is plain: scope in writing, "
        "authorization before you start, and a log you would be comfortable handing to a court. \"It was all public\" describes where the data "
        "came from. It says nothing about whether you were entitled to collect it.\n")
    out.append("OSINT is a research discipline wearing a hacker's clothes. The tools change every year, but pivoting, corroboration, capture and the passive/active line do not.\n")
    out.append("## Contributing\n")
    out.append(
        "Tool suggestions, corrections and dead-link reports are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the inclusion bar and how to "
        "edit the data; the README and every page under `docs/` are generated from `data/tools.yml`, so edit that file and run "
        "`python scripts/build_readme.py`. Security issues: see [SECURITY.md](SECURITY.md).\n")
    out.append("## License\n")
    out.append("Code under the [MIT License](LICENSE). Guide text and data under [CC BY 4.0](LICENSE-CONTENT.md). Tool names are trademarks of their owners.\n")
    return "\n".join(out)


def build():
    sections, tools, skips = load()
    errs = validate(sections, tools, skips)
    if errs:
        raise SystemExit("data invalid:\n  " + "\n  ".join(errs))
    files = {ROOT / "README.md": render_readme(sections, tools, skips)}
    for i, s in enumerate(sections):
        prev_s = sections[i - 1] if i > 0 else None
        next_s = sections[i + 1] if i + 1 < len(sections) else None
        if s["id"] == SKIP_SLUG:
            files[ROOT / "docs" / ("%s.md" % s["id"])] = render_skip_page(s, skips, sections, prev_s)
        else:
            files[ROOT / "docs" / ("%s.md" % s["id"])] = render_section_page(s, tools, sections, prev_s, next_s)
    return files


def main(argv):
    files = build()
    check = "--check" in argv
    stale = []
    for path, text in files.items():
        if not text.endswith("\n"):
            text += "\n"
        files[path] = text
        cur = path.read_text(encoding="utf8") if path.exists() else None
        if cur != text:
            stale.append(path)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf8")
    if check:
        if stale:
            print("out of date (run python scripts/build_readme.py):")
            for p in stale:
                print("  ", p.relative_to(ROOT))
            return 1
        print("ok: generated files are up to date")
        return 0
    print("wrote %d file(s), %d unchanged" % (len(stale), len(files) - len(stale)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
