#!/usr/bin/env python3
"""Generate docs/tools.json: every tool in the guide, for other sites to list and filter.

    python scripts/build_tools_json.py          write the file
    python scripts/build_tools_json.py --check  exit 1 if it is out of date

All tools are named. Entries in the gated tier carry only a name, section, tier and a link to the guide entry, with no
summary, kind or other detail: the point of the gated tier is that the detail lives in the guide, behind its caution.
`reach` lists the pivot-map data types from which a tool can be reached (empty for gated tools, which the map never names).
"""
import json
import sys

from osintlib import ROOT, TIERS, load, load_pivots, real_tools, validate_pivots

REPO = "https://github.com/iijarrett/osint-field-guide"
OUT = ROOT / "docs" / "tools.json"


def build_data():
    sections, tools, _ = load()
    pivots = load_pivots()
    errs = validate_pivots(pivots, sections, tools)
    if errs:
        raise SystemExit("pivots.yml is invalid; run python scripts/validate.py\n" + "\n".join(errs))
    reach = {}
    for e in pivots["edges"]:
        for tid in e["via"]:
            reach.setdefault(tid, [])
            if e["from"] not in reach[tid]:
                reach[tid].append(e["from"])
    node_order = [n["id"] for n in pivots["nodes"]]
    sec_title = {s["id"]: s["title"] for s in sections}
    used = []
    items = []
    for t in real_tools(tools):
        entry = {
            "id": t["id"], "name": t["name"], "section": t["section"], "tier": t["tier"],
            "url": "%s/blob/main/docs/%s.md#%s" % (REPO, t["section"], t["id"]),
        }
        if t["tier"] != "gated":
            entry["kind"] = t["kind"]
            entry["summary"] = t["summary"]
            entry["verified"] = str(t["verified"]["date"])
            entry["reach"] = sorted(reach.get(t["id"], []), key=node_order.index)
        else:
            entry["reach"] = []
        if t["section"] not in used:
            used.append(t["section"])
        items.append(entry)
    secs = [{"id": s["id"], "rank": s["rank"], "title": sec_title[s["id"]]} for s in sections if s["id"] in used]
    counts = {k: sum(1 for i in items if i["tier"] == k) for k in TIERS}
    return {"toolCount": len(items), "tierCounts": counts, "sections": secs, "tools": items}


def build():
    return {OUT: json.dumps(build_data(), ensure_ascii=False, indent=2) + "\n"}


def main(argv):
    files = build()
    check = "--check" in argv
    stale = [p for p, text in files.items() if not p.exists() or p.read_text(encoding="utf8") != text]
    if check:
        if stale:
            print("out of date (run python scripts/build_tools_json.py):")
            for p in stale:
                print("  ", p.relative_to(ROOT))
            return 1
        print("ok: tools.json is up to date")
        return 0
    for p in stale:
        p.write_text(files[p], encoding="utf8")
    print("wrote %d file(s), %d unchanged" % (len(stale), len(files) - len(stale)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
