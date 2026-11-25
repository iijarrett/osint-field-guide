import copy
import json

import build_pivot_map as pm
from osintlib import ROOT, load, load_pivots, validate_pivots


def test_pivots_validate():
    sections, tools, _ = load()
    assert validate_pivots(load_pivots(), sections, tools) == []


def test_no_gated_tool_on_the_map():
    sections, tools, _ = load()
    gated = {t["id"] for t in tools if t.get("tier") == "gated"}
    for e in load_pivots()["edges"]:
        assert not gated & set(e["via"])


def test_generated_files_are_current():
    for path, text in pm.build().items():
        if not text.endswith("\n"):
            text += "\n"
        assert path.exists(), "%s missing; run python scripts/build_pivot_map.py" % path
        assert path.read_text(encoding="utf8") == text, "%s is out of date; run python scripts/build_pivot_map.py" % path.relative_to(ROOT)


def test_page_is_self_contained():
    page = (ROOT / "docs" / "pivot-map.html").read_text(encoding="utf8")
    for bad in ("src=\"http", "href=\"//", "@import", "fetch(", "XMLHttpRequest"):
        assert bad not in page, bad
    # the only absolute links are anchors the reader clicks, never loaded resources
    assert "<link " not in page and "<img" not in page


def test_json_matches_data():
    g = json.loads((ROOT / "docs" / "pivot-map.json").read_text(encoding="utf8"))
    p = load_pivots()
    assert [n["id"] for n in g["nodes"]] == [n["id"] for n in p["nodes"]]
    assert len(g["edges"]) == len(p["edges"])
    for e in g["edges"]:
        for t in e["tools"]:
            assert t["url"].startswith("https://github.com/iijarrett/osint-field-guide/blob/main/docs/")
            assert t["tier"] in ("start", "deeper")


def _bad(mutate):
    sections, tools, _ = load()
    p = copy.deepcopy(load_pivots())
    mutate(p)
    return validate_pivots(p, sections, tools)


def test_rejects_unknown_node_and_tool():
    assert any("unknown node" in e for e in _bad(lambda p: p["edges"][0].update({"to": "nowhere"})))
    assert any("unknown tool" in e for e in _bad(lambda p: p["edges"][0].update({"via": ["no-such-tool"]})))


def test_rejects_gated_and_step_tools():
    assert any("gated" in e for e in _bad(lambda p: p["edges"][0].update({"via": ["people-search"]})))
    assert any("workflow step" in e for e in _bad(lambda p: p["edges"][0].update({"via": ["loop-pivot"]})))


def test_rejects_orphan_node_and_duplicate_edge():
    def orphan(p):
        p["nodes"].append({"id": "lonely", "label": "x", "short": "x", "section": "01-username"})
    assert any("no edges" in e for e in _bad(orphan))
    assert any("duplicate edge" in e for e in _bad(lambda p: p["edges"].append(dict(p["edges"][0]))))
