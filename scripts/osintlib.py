"""Shared loading and validation for the guide data."""
import datetime
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

TIERS = {"start": "Start here", "deeper": "Go deeper", "gated": "Gated"}
REQUIRED = ("id", "name", "section", "kind", "summary", "what")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
GH_RE = re.compile(r"^[\w.-]+/[\w.-]+$")
ASSUMES = (
    "Install lines assume Windows 11 (PowerShell, winget), macOS (Homebrew) and Debian, Ubuntu or Kali (apt). "
    "A row labelled All OS is the same command everywhere."
)


def _read(name):
    with open(DATA / name, encoding="utf8") as f:
        return yaml.safe_load(f)


def load():
    return _read("sections.yml"), _read("tools.yml"), _read("skip.yml")


def real_tools(tools):
    """Entries that are tools, not workflow steps."""
    return [t for t in tools if not t.get("step")]


def validate(sections, tools, skips):
    errs = []
    sec_ids = [s.get("id") for s in sections]
    if len(sec_ids) != len(set(sec_ids)):
        errs.append("duplicate section ids")
    for s in sections:
        for k in ("id", "rank", "title"):
            if not s.get(k):
                errs.append("section %r missing %s" % (s.get("id"), k))
    seen = set()
    for t in tools:
        tid = t.get("id", "<no id>")
        if tid in seen:
            errs.append("duplicate tool id: %s" % tid)
        seen.add(tid)
        if not isinstance(tid, str) or not SLUG_RE.match(tid):
            errs.append("%s: id must be a lowercase slug" % tid)
        for k in REQUIRED:
            if not t.get(k):
                errs.append("%s: missing %s" % (tid, k))
        if t.get("section") not in sec_ids:
            errs.append("%s: unknown section %r" % (tid, t.get("section")))
        if not t.get("step") and t.get("tier") not in TIERS:
            errs.append("%s: tier must be one of %s" % (tid, ", ".join(TIERS)))
        for row in t.get("install", []) or []:
            if not row.get("os"):
                if not row.get("cmd") and not row.get("note"):
                    errs.append("%s: empty install row" % tid)
            elif not (row.get("cmd") or row.get("note")):
                errs.append("%s: install row %r has no cmd or note" % (tid, row.get("os")))
            cmd = row.get("cmd") or ""
            if re.search(r"curl[^|]*\|\s*(ba)?sh|wget[^|]*\|\s*(ba)?sh|iwr[^|]*\|\s*iex", cmd):
                errs.append("%s: piped-to-shell installer is not allowed (%r)" % (tid, cmd[:40]))
        for l in t.get("links", []) or []:
            u = l.get("url", "")
            if not u.startswith("https://"):
                errs.append("%s: link must be https: %r" % (tid, u))
            if not l.get("label"):
                errs.append("%s: link missing label" % tid)
        gh = t.get("github")
        if gh and not GH_RE.match(gh):
            errs.append("%s: github must be owner/repo" % tid)
        v = t.get("verified")
        if not t.get("step"):
            if not v or "date" not in v:
                errs.append("%s: missing verified.date" % tid)
            else:
                try:
                    datetime.date.fromisoformat(str(v["date"]))
                except ValueError:
                    errs.append("%s: verified.date must be YYYY-MM-DD" % tid)
                if v.get("install_checked") not in ("yes", "partial", "no", None):
                    errs.append("%s: install_checked must be yes, partial or no" % tid)
        c = t.get("caution")
        if c is not None and not (c.get("title") or c.get("body")):
            errs.append("%s: empty caution" % tid)
    for i, s in enumerate(skips):
        if not s.get("name") or not s.get("why"):
            errs.append("skip entry %d needs name and why" % i)
    return errs
