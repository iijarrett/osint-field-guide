#!/usr/bin/env python3
"""Generate docs/pivot-map.html and docs/pivot-map.json from data/pivots.yml and data/tools.yml.

    python scripts/build_pivot_map.py          write the files
    python scripts/build_pivot_map.py --check  exit 1 if either file is out of date

The HTML is one self-contained file: fonts, styles, data and script are all inline, and the page makes no network
requests. The JSON is the same graph with tool names and links resolved, for other sites to render in their own style.
"""
import base64
import html
import json
import sys
from pathlib import Path

from osintlib import ROOT, load, load_pivots, real_tools, validate_pivots

REPO = "https://github.com/iijarrett/osint-field-guide"
HERE = Path(__file__).resolve().parent
OUT_HTML = ROOT / "docs" / "pivot-map.html"
OUT_JSON = ROOT / "docs" / "pivot-map.json"

FONTS = [
    ("IBM Plex Sans", 300, "ibm-plex-sans-latin-300-normal.woff2"),
    ("IBM Plex Sans", 400, "ibm-plex-sans-latin-400-normal.woff2"),
    ("IBM Plex Sans", 600, "ibm-plex-sans-latin-600-normal.woff2"),
    ("JetBrains Mono", 400, "jetbrains-mono-latin-400-normal.woff2"),
    ("JetBrains Mono", 600, "jetbrains-mono-latin-600-normal.woff2"),
]


def font_css():
    out = []
    for family, weight, fname in FONTS:
        b64 = base64.b64encode((HERE / "fonts" / fname).read_bytes()).decode("ascii")
        out.append(
            "@font-face{font-family:'%s';font-weight:%d;font-style:normal;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}" % (family, weight, b64)
        )
    return "\n".join(out)


def graph():
    """The pivot graph with each tool resolved to its name, tier and documentation link."""
    sections, tools, _ = load()
    pivots = load_pivots()
    errs = validate_pivots(pivots, sections, tools)
    if errs:
        raise SystemExit("pivots.yml is invalid; run python scripts/validate.py\n" + "\n".join(errs))
    by_id = {t["id"]: t for t in tools}
    nodes = []
    for n in pivots["nodes"]:
        nodes.append({
            "id": n["id"], "label": n["label"], "short": n["short"],
            "guide": "%s/blob/main/docs/%s.md" % (REPO, n["section"]),
        })
    edges = []
    for e in pivots["edges"]:
        resolved = []
        for tid in e["via"]:
            t = by_id[tid]
            resolved.append({
                "id": tid, "name": t["name"], "tier": t["tier"],
                "url": "%s/blob/main/docs/%s.md#%s" % (REPO, t["section"], tid),
            })
        item = {"from": e["from"], "to": e["to"], "label": e["label"], "tools": resolved}
        if e.get("note"):
            item["note"] = e["note"]
        edges.append(item)
    return {"nodes": nodes, "edges": edges, "toolCount": len(real_tools(tools))}


def static_list(g):
    """Plain HTML list for readers without JavaScript."""
    by = {n["id"]: n for n in g["nodes"]}
    parts = ["<h2>All pivots</h2>"]
    for n in g["nodes"]:
        rows = [e for e in g["edges"] if e["from"] == n["id"]]
        if not rows:
            continue
        parts.append("<h3>From %s</h3><ul>" % html.escape(n["label"][0].lower() + n["label"][1:]))
        for e in rows:
            tools = ", ".join('<a href="%s">%s</a>' % (html.escape(t["url"]), html.escape(t["name"])) for t in e["tools"])
            parts.append("<li>%s: %s (%s)</li>" % (html.escape(by[e["to"]]["short"]), html.escape(e["label"]), tools))
        parts.append("</ul>")
    return "".join(parts)


def build():
    g = graph()
    data_json = json.dumps(g, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (HERE / "pivot_template.html").read_text(encoding="utf8")
    page = page.replace("/*FONTS*/", font_css()).replace("/*STATIC*/", static_list(g)).replace("/*DATA*/", data_json)
    pretty = json.dumps(g, ensure_ascii=False, indent=2) + "\n"
    return {OUT_HTML: page, OUT_JSON: pretty}


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
            print("out of date (run python scripts/build_pivot_map.py):")
            for p in stale:
                print("  ", p.relative_to(ROOT))
            return 1
        print("ok: pivot map files are up to date")
        return 0
    print("wrote %d file(s), %d unchanged" % (len(stale), len(files) - len(stale)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
