import json

import pytest

from osintguide import cli


@pytest.fixture(scope="module")
def data():
    return cli.load()


def run(capsys, *argv):
    rc = cli.main(list(argv))
    return rc, capsys.readouterr().out


def test_row_applies_matrix():
    ra = cli.row_applies
    assert ra("Windows", "windows") and not ra("Windows", "linux")
    assert ra("macOS/Linux", "macos") and ra("macOS/Linux", "linux") and not ra("macOS/Linux", "windows")
    assert ra("Win/Linux", "windows") and ra("Win/Linux", "linux") and not ra("Win/Linux", "macos")
    assert ra("Kali", "linux") and not ra("Kali", "macos")
    assert ra("Hash: Mac", "macos") and not ra("Hash: Mac", "windows")
    for neutral in ("All OS", "Any OS", "Run", "Then", "Check", "Docker", "", None):
        assert all(ra(neutral, o) for o in cli.OS_CHOICES)


def test_every_tool_has_a_row_for_each_os_or_none(data):
    # filtering must never drop everything for a tool that has install rows with a neutral label
    _, tools = data
    for t in tools:
        rows = t.get("install") or []
        if rows and all(not any(k in (r.get("os") or "").lower() for k in ("win", "mac", "linux", "kali")) for r in rows):
            for o in cli.OS_CHOICES:
                assert cli.install_rows(t, o) == rows


def test_sections_counts_add_up(data, capsys):
    rc, out = run(capsys, "sections", "--json")
    rows = json.loads(out)
    assert rc == 0 and sum(r["entries"] for r in rows) == len(data[1])


def test_list_filters(capsys):
    _, out = run(capsys, "list", "--tier", "gated", "--json")
    ids = {r["id"] for r in json.loads(out)}
    assert "face-search" in ids and "maigret" not in ids
    _, out = run(capsys, "list", "--section", "1", "--json")
    assert all(r["section"] == "01-username" for r in json.loads(out))


def test_search_all_terms_must_match(capsys):
    _, out = run(capsys, "search", "username", "dossier", "--json")
    ids = {r["id"] for r in json.loads(out)}
    assert "maigret" in ids
    rc, out = run(capsys, "search", "zzzznotathing")
    assert rc == 1 and "Nothing matches" in out


def test_show_prints_caution_for_gated(capsys):
    rc, out = run(capsys, "show", "face-search")
    assert rc == 0 and "CAUTION" in out and "does not run anything" in out


def test_show_hides_markdown_markers(capsys):
    _, out = run(capsys, "show", "maigret", "--os", "linux")
    assert "**" not in out


def test_install_filters_by_os(capsys):
    _, win = run(capsys, "install", "bench-case", "--os", "windows")
    _, mac = run(capsys, "install", "bench-case", "--os", "macos")
    assert "New-Item" in win and "mkdir" not in win
    assert "mkdir" in mac and "New-Item" not in mac
    _, every = run(capsys, "install", "bench-case", "--all-os")
    assert "New-Item" in every and "mkdir" in every


def test_install_json_and_prefix_lookup(capsys):
    _, out = run(capsys, "install", "maigret", "--os", "linux", "--json")
    d = json.loads(out)
    assert d["id"] == "maigret" and any("pipx install maigret" == r.get("cmd") for r in d["install"])


def test_unknown_and_ambiguous_ids_exit(capsys):
    with pytest.raises(SystemExit):
        cli.main(["show", "definitely-not-an-entry"])
    with pytest.raises(SystemExit):
        cli.main(["show", "-"])  # matches many ids


def test_never_executes_anything(monkeypatch, capsys):
    import subprocess
    import os

    def boom(*a, **k):
        raise AssertionError("the CLI must not run commands")

    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(os, "system", boom)
    run(capsys, "install", "maigret", "--os", "linux")


def test_data_dir_override(tmp_path, monkeypatch):
    monkeypatch.setenv("OSINT_GUIDE_DATA", str(tmp_path))
    assert cli.find_data_dir().name == "data"  # empty override is ignored, falls back to the checkout
