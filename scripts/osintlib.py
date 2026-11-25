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


def load_ignore():
    """Accepted health-check exceptions: [{url, reason, until}]. Missing file means none."""
    try:
        return _read("health_ignore.yml") or []
    except FileNotFoundError:
        return []


def load_pivots():
    """Pivot map data: {nodes: [...], edges: [...]}."""
    return _read("pivots.yml")


def validate_pivots(pivots, sections, tools):
    """Every edge must connect real nodes through real, non-gated tools."""
    errs = []
    nodes = pivots.get("nodes") or []
    edges = pivots.get("edges") or []
    sec_ids = {s["id"] for s in sections}
    by_id = {t["id"]: t for t in tools}
    node_ids = [n.get("id") for n in nodes]
    if len(node_ids) != len(set(node_ids)):
        errs.append("pivots: duplicate node ids")
    for n in nodes:
        nid = n.get("id", "<no id>")
        if not isinstance(nid, str) or not SLUG_RE.match(nid):
            errs.append("pivots node %s: id must be a lowercase slug" % nid)
        for k in ("label", "short", "section"):
            if not n.get(k):
                errs.append("pivots node %s: missing %s" % (nid, k))
        if n.get("section") and n["section"] not in sec_ids:
            errs.append("pivots node %s: unknown section %r" % (nid, n["section"]))
    ids = set(node_ids)
    touched = set()
    seen = set()
    for i, e in enumerate(edges):
        where = "pivots edge %d (%s -> %s)" % (i, e.get("from"), e.get("to"))
        for k in ("from", "to"):
            if e.get(k) not in ids:
                errs.append("%s: unknown node %r in %s" % (where, e.get(k), k))
            else:
                touched.add(e[k])
        via = e.get("via")
        if not via or not isinstance(via, list):
            errs.append("%s: via must be a non-empty list of tool ids" % where)
            via = []
        for tid in via:
            t = by_id.get(tid)
            if t is None:
                errs.append("%s: unknown tool %r" % (where, tid))
            elif t.get("step"):
                errs.append("%s: %r is a workflow step, not a tool" % (where, tid))
            elif t.get("tier") == "gated":
                errs.append("%s: %r is gated; the map must not name gated tools" % (where, tid))
        if len(via) != len(set(via)):
            errs.append("%s: repeated tool in via" % where)
        label = e.get("label") or ""
        if not label:
            errs.append("%s: missing label" % where)
        elif len(label) > 140:
            errs.append("%s: label is longer than 140 characters" % where)
        key = (e.get("from"), e.get("to"), tuple(sorted(via)))
        if key in seen:
            errs.append("%s: duplicate edge" % where)
        seen.add(key)
    for nid in ids - touched:
        errs.append("pivots node %s: has no edges" % nid)
    return errs


def validate_ignore(rows, today=None):
    """Each exception needs a url, a reason and an expiry date, so nothing is ignored forever."""
    today = today or datetime.date.today()
    errs = []
    for i, r in enumerate(rows):
        label = r.get("url") or "row %d" % i
        if not str(r.get("url", "")).startswith("https://"):
            errs.append("health_ignore %s: url must be https" % label)
        if not r.get("reason"):
            errs.append("health_ignore %s: missing reason" % label)
        try:
            until = datetime.date.fromisoformat(str(r.get("until")))
            if (until - today).days > 180:
                errs.append("health_ignore %s: until is more than 180 days away; accepted exceptions must be re-reviewed" % label)
        except ValueError:
            errs.append("health_ignore %s: until must be YYYY-MM-DD" % label)
    return errs


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
            if "<" in u or ">" in u or " " in u:
                errs.append("%s: link looks like a placeholder or contains a space: %r" % (tid, u))
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
