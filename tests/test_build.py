import build_readme as b
from osintlib import ROOT, load, real_tools


def test_generated_files_are_current():
    for path, text in b.build().items():
        if not text.endswith("\n"):
            text += "\n"
        assert path.exists(), "%s missing; run python scripts/build_readme.py" % path
        assert path.read_text(encoding="utf8") == text, "%s is out of date; run python scripts/build_readme.py" % path.relative_to(ROOT)


def test_readme_lists_every_tool():
    sections, tools, skips = load()
    readme = (ROOT / "README.md").read_text(encoding="utf8")
    for t in real_tools(tools):
        assert "#%s)" % t["id"] in readme, t["id"]


def test_section_refs_become_links():
    sections, _, _ = load()
    out = b.link_refs("see §05 and §99", sections, "")
    assert "[§05](05-domain-ip-network.md)" in out
    assert "§99" in out and "[§99]" not in out


def test_install_block_groups_by_os():
    block = b.install_block([
        {"os": "All OS", "cmd": "pipx install x"},
        {"os": "Run", "cmd": "x --help", "note": "prints usage"},
        {"os": "Linux", "note": "already installed on Kali"},
    ])
    assert block.startswith("```sh\n# All OS\npipx install x\n# Run\nx --help\n#   prints usage\n")
    assert "# Linux: already installed on Kali" in block
