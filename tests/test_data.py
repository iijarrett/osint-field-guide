import copy
import re

import pytest

from osintlib import load, real_tools, validate


@pytest.fixture(scope="module")
def data():
    return load()


def test_data_validates(data):
    assert validate(*data) == []


def test_ids_unique(data):
    ids = [t["id"] for t in data[1]]
    assert len(ids) == len(set(ids))


def test_every_section_has_content(data):
    sections, tools, skips = data
    used = {t["section"] for t in tools}
    for s in sections:
        if s["id"].endswith("skip"):
            assert skips
        else:
            assert s["id"] in used, "section %s has no tools" % s["id"]


def test_no_piped_installers(data):
    for t in data[1]:
        for row in t.get("install", []) or []:
            assert not re.search(r"\|\s*(ba)?sh\b", row.get("cmd", "")), t["id"]


def test_no_private_references(data):
    text = repr(data)
    for term in ("Analyst Bench", "OpSec Field Guide", "Privacy & Anonymity Guide"):
        assert term not in text


@pytest.mark.parametrize("mutate,fragment", [
    (lambda t: t[0].pop("summary"), "missing summary"),
    (lambda t: t[1].update(id=t[0]["id"]), "duplicate tool id"),
    (lambda t: t[1].update(section="nope"), "unknown section"),
    (lambda t: t[12].update(tier="best"), "tier must be"),
    (lambda t: t[12].update(links=[{"label": "x", "url": "http://example.com"}]), "must be https"),
    (lambda t: t[12].update(install=[{"os": "All OS", "cmd": "curl https://x.sh | bash"}]), "piped-to-shell"),
    (lambda t: t[12].update(github="not a repo"), "owner/repo"),
    (lambda t: t[12].update(verified={"date": "yesterday"}), "YYYY-MM-DD"),
])
def test_validator_catches_problems(data, mutate, fragment):
    sections, tools, skips = copy.deepcopy(data)
    mutate(tools)
    errs = validate(sections, tools, skips)
    assert any(fragment in e for e in errs), errs


def test_placeholder_links_are_rejected(data):
    sections, tools, skips = copy.deepcopy(data)
    tools[0]["links"] = [{"label": "x", "url": "https://github.com/<org"}]
    assert any("placeholder" in e for e in validate(sections, tools, skips))


def test_health_ignore_file_is_valid_and_expires():
    import datetime
    from osintlib import load_ignore, validate_ignore
    today = datetime.date(2026, 11, 25)
    assert validate_ignore(load_ignore(), today) == []
    far = [{"url": "https://a.com/", "reason": "x", "until": "2030-01-01"}]
    assert any("180 days" in e for e in validate_ignore(far, today))
    assert any("missing reason" in e for e in validate_ignore([{"url": "https://a.com/", "until": "2026-12-01"}], today))
