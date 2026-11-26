import json

import build_tools_json as tj
from osintlib import ROOT, load, real_tools

GATED_DETAIL_FIELDS = ("summary", "kind", "verified", "what", "why", "caution", "install", "links", "github", "notes")


def test_generated_file_is_current():
    for path, text in tj.build().items():
        assert path.exists(), "%s missing; run python scripts/build_tools_json.py" % path
        assert path.read_text(encoding="utf8") == text, "%s is out of date; run python scripts/build_tools_json.py" % path.relative_to(ROOT)


def test_every_tool_is_named_once():
    g = json.loads((ROOT / "docs" / "tools.json").read_text(encoding="utf8"))
    _, tools, _ = load()
    assert [t["id"] for t in g["tools"]] == [t["id"] for t in real_tools(tools)]
    assert g["toolCount"] == len(g["tools"]) == len(real_tools(tools))
    assert sum(g["tierCounts"].values()) == g["toolCount"]


def test_gated_entries_carry_no_detail():
    g = json.loads((ROOT / "docs" / "tools.json").read_text(encoding="utf8"))
    gated = [t for t in g["tools"] if t["tier"] == "gated"]
    assert gated, "expected a gated tier"
    for t in gated:
        assert set(t) == {"id", "name", "section", "tier", "url", "reach"}, t["id"]
        assert t["reach"] == []


def test_open_entries_have_summary_and_links():
    g = json.loads((ROOT / "docs" / "tools.json").read_text(encoding="utf8"))
    sec_ids = {s["id"] for s in g["sections"]}
    for t in g["tools"]:
        assert t["section"] in sec_ids
        assert t["url"].startswith("https://github.com/iijarrett/osint-field-guide/blob/main/docs/")
        if t["tier"] != "gated":
            assert t["summary"] and t["kind"] and t["verified"]
