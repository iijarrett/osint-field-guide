"""osint-guide: look up tools, install lines and cautions from the guide, offline.

The command only reads the guide data and prints. It never runs an install line and
never makes a network request. Read a line, then decide whether to run it.

    osint-guide sections
    osint-guide list [--section 05] [--tier start] [--search email]
    osint-guide search "reverse image"
    osint-guide show maigret
    osint-guide install maigret --os linux
"""
import argparse
import json
import os
import platform
import re
import shutil
import sys
import textwrap
from pathlib import Path

import yaml

from . import __version__

TIERS = ("start", "deeper", "gated")
OS_CHOICES = ("windows", "macos", "linux")


def find_data_dir():
    """Locate data/. Order: $OSINT_GUIDE_DATA, a copy bundled in the wheel, the repository checkout."""
    candidates = []
    env = os.environ.get("OSINT_GUIDE_DATA")
    if env:
        candidates.append(Path(env))
    here = Path(__file__).resolve().parent
    candidates += [here / "data", here.parent / "data"]
    for c in candidates:
        if (c / "tools.yml").is_file() and (c / "sections.yml").is_file():
            return c
    raise SystemExit("osint-guide: cannot find the data folder. Set OSINT_GUIDE_DATA to a folder holding tools.yml and sections.yml.")


def load(data_dir=None):
    d = Path(data_dir) if data_dir else find_data_dir()
    out = []
    for name in ("sections.yml", "tools.yml"):
        with open(d / name, encoding="utf8") as f:
            out.append(yaml.safe_load(f))
    return out[0], out[1]


def detect_os():
    return {"Windows": "windows", "Darwin": "macos"}.get(platform.system(), "linux")


def row_applies(label, target):
    """Does an install row with this label apply to the target OS?

    Labels like "Run", "Then" or "Check" continue a sequence and always apply. Labels naming an OS
    ("Windows", "macOS/Linux", "Kali", "Hash: Mac") apply only to the OS they name. "All OS" always applies.
    """
    low = (label or "").lower()
    named = set()
    if "win" in low:
        named.add("windows")
    if "mac" in low:
        named.add("macos")
    if "linux" in low or "kali" in low or "debian" in low or "ubuntu" in low:
        named.add("linux")
    if not named:
        return True
    return target in named


def install_rows(tool, target):
    rows = tool.get("install") or []
    if target is None:
        return rows
    return [r for r in rows if row_applies(r.get("os"), target)]


def find_tool(tools, ident):
    ident = ident.lower().strip()
    for t in tools:
        if t["id"] == ident:
            return t
    hits = [t for t in tools if ident in t["id"] or ident in t["name"].lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit("osint-guide: no entry matches %r. Try: osint-guide search %s" % (ident, ident))
    raise SystemExit("osint-guide: %r matches several entries: %s" % (ident, ", ".join(t["id"] for t in hits)))


def section_matches(sec, want):
    return sec["id"] == want or sec["id"].startswith(want + "-") or sec["id"].split("-")[0] == want.zfill(2)


def haystack(t):
    parts = [t["id"], t["name"], t.get("summary", ""), t.get("what", ""), t.get("why", ""), t.get("kind", "")]
    return " ".join(str(p) for p in parts).lower()


def width():
    return max(60, min(100, shutil.get_terminal_size((88, 24)).columns))


def plain(text):
    """Drop Markdown emphasis markers; the guide data uses **bold** and *italic*."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", str(text))
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", text)


def wrap(text, indent="  "):
    return textwrap.fill(" ".join(plain(text).split()), width=width(), initial_indent=indent, subsequent_indent=indent)


def tier_label(t):
    return "step" if t.get("step") else t.get("tier", "-")


def emit_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def cmd_sections(args, sections, tools):
    counts = {}
    for t in tools:
        counts[t["section"]] = counts.get(t["section"], 0) + 1
    rows = [{"id": s["id"], "title": s["title"], "entries": counts.get(s["id"], 0)} for s in sections]
    if args.json:
        return emit_json(rows)
    for r in rows:
        print("%-24s %3d  %s" % (r["id"], r["entries"], r["title"]))


def select(args, sections, tools):
    chosen = tools
    if getattr(args, "section", None):
        ids = {s["id"] for s in sections if section_matches(s, args.section)}
        if not ids:
            raise SystemExit("osint-guide: no section matches %r. Run: osint-guide sections" % args.section)
        chosen = [t for t in chosen if t["section"] in ids]
    if getattr(args, "tier", None):
        chosen = [t for t in chosen if t.get("tier") == args.tier]
    terms = (getattr(args, "search", None) or getattr(args, "terms", None) or "")
    terms = terms.lower().split() if isinstance(terms, str) else [w.lower() for w in terms]
    for w in terms:
        chosen = [t for t in chosen if w in haystack(t)]
    return chosen


def cmd_list(args, sections, tools):
    chosen = select(args, sections, tools)
    if args.json:
        return emit_json([{"id": t["id"], "name": t["name"], "section": t["section"], "tier": tier_label(t), "summary": t.get("summary", "")} for t in chosen])
    if not chosen:
        print("Nothing matches.")
        return 1
    titles = {s["id"]: s["title"] for s in sections}
    last = None
    for t in chosen:
        if t["section"] != last:
            last = t["section"]
            print("\n%s  %s" % (last, titles.get(last, "")))
        print("  %-20s %-7s %s" % (t["id"], tier_label(t), t["name"]))
    print("\n%d entries. Details: osint-guide show <id>" % len(chosen))


def cmd_search(args, sections, tools):
    return cmd_list(args, sections, tools)


def show_install(tool, target, indent="  "):
    rows = install_rows(tool, target)
    if not rows:
        return
    print("\nInstall%s" % (" (%s)" % target if target else ""))
    for r in rows:
        label = r.get("os") or ""
        cmd = r.get("cmd")
        note = r.get("note")
        if cmd:
            if label:
                print("%s# %s" % (indent, label))
            for line in str(cmd).splitlines():
                print(indent + line)
        if note:
            print(wrap(("%s: %s" % (label, note)) if label and not cmd else note, indent + "  "))


def cmd_show(args, sections, tools):
    t = find_tool(tools, args.id)
    target = None if args.all_os else (args.os or detect_os())
    if args.json:
        d = dict(t)
        d["install"] = install_rows(t, target)
        return emit_json(d)
    titles = {s["id"]: s["title"] for s in sections}
    print("%s  [%s]" % (t["name"], t["id"]))
    print("%s  ·  %s  ·  %s" % (titles.get(t["section"], t["section"]), tier_label(t), t.get("kind", "")))
    c = t.get("caution")
    if c:
        print("\nCAUTION: %s" % (c.get("title") or ""))
        print(wrap(c.get("body") or ""))
    print()
    print(wrap(t.get("what", "")))
    if t.get("why"):
        print()
        print(wrap(t["why"]))
    show_install(t, target)
    for n in t.get("notes") or []:
        print()
        print(wrap(n))
    links = t.get("links") or []
    if links:
        print("\nLinks")
        for l in links:
            print("  %s  %s" % (l["label"], l["url"]))
    v = t.get("verified") or {}
    if v:
        line = "Reviewed %s" % v.get("date", "?")
        if t.get("install") and v.get("install_checked"):
            line += "; install lines " + {"yes": "checked", "partial": "partly checked", "no": "not checked"}.get(v["install_checked"], "not recorded")
        print("\n" + line + ".")
    print("\nThis command only prints. It does not run anything.")


def cmd_install(args, sections, tools):
    t = find_tool(tools, args.id)
    target = None if args.all_os else (args.os or detect_os())
    rows = install_rows(t, target)
    if args.json:
        return emit_json({"id": t["id"], "os": target, "install": rows})
    if t.get("caution"):
        print("# CAUTION: %s. Read the entry first: osint-guide show %s" % (t["caution"].get("title") or "gated tool", t["id"]))
    if not rows:
        print("# %s has no install line (it is a site, a practice or a workflow step). Run: osint-guide show %s" % (t["id"], t["id"]))
        return 1
    for r in rows:
        if r.get("cmd"):
            if r.get("os"):
                print("# %s" % r["os"])
            print(r["cmd"])
        elif r.get("note"):
            print("# %s" % (("%s: %s" % (r["os"], r["note"])) if r.get("os") else r["note"]))


def build_parser():
    p = argparse.ArgumentParser(prog="osint-guide", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version="osint-guide " + __version__)
    p.add_argument("--data", help="folder holding tools.yml and sections.yml (default: bundled or repository copy)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sections", help="list the guide sections and how many entries each has")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_sections)

    s = sub.add_parser("list", help="list entries, optionally filtered")
    s.add_argument("--section", help="section number or id, for example 05 or 05-domain-ip-network")
    s.add_argument("--tier", choices=TIERS)
    s.add_argument("--search", help="words that must all appear in the entry")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("search", help="find entries by word")
    s.add_argument("terms", nargs="+")
    s.add_argument("--section")
    s.add_argument("--tier", choices=TIERS)
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_search)

    for name, fn, help_ in (("show", cmd_show, "show one entry in full"), ("install", cmd_install, "print only the install lines for one entry")):
        s = sub.add_parser(name, help=help_)
        s.add_argument("id", help="entry id (a unique part of the id or name also works)")
        s.add_argument("--os", choices=OS_CHOICES, help="default: the OS you are on")
        s.add_argument("--all-os", action="store_true", help="show every OS row")
        s.add_argument("--json", action="store_true")
        s.set_defaults(fn=fn)
    return p


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    if args.cmd == "search":
        args.search = None
    sections, tools = load(args.data)
    try:
        return args.fn(args, sections, tools) or 0
    except BrokenPipeError:  # for example `osint-guide list | head`
        try:
            sys.stdout = open(os.devnull, "w")
        except OSError:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
