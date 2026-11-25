import datetime

import health_check as h

TODAY = datetime.date(2026, 11, 23)


def fake_fetch(mapping):
    def f(url, method="GET"):
        return mapping.get(url, (0, None))
    return f


def check(url, mapping):
    return h.check_url(url, fetcher=fake_fetch(mapping), retries=1, sleep=lambda s: None)


def test_ok():
    r = check("https://a.com/", {"https://a.com/": (200, "https://a.com/")})
    assert r["state"] == "ok"


def test_dead_on_404_and_no_response():
    assert check("https://a.com/x", {"https://a.com/x": (404, "https://a.com/x")})["state"] == "dead"
    assert check("https://gone.example/", {})["state"] == "dead"


def test_bot_block_is_unknown_not_dead():
    r = check("https://a.com/", {"https://a.com/": (403, "https://a.com/")})
    assert r["state"] == "unknown"


def test_moved_domain_detected_but_www_is_not():
    moved = check("https://a.com/", {"https://a.com/": (200, "https://intel471.com/")})
    assert moved["state"] == "moved"
    same = check("https://a.com/", {"https://a.com/": (200, "https://www.a.com/")})
    assert same["state"] == "ok"


def test_retry_recovers():
    calls = []

    def flaky(url, method="GET"):
        calls.append(1)
        return (0, None) if len(calls) == 1 else (200, url)

    r = h.check_url("https://a.com/", fetcher=flaky, retries=2, sleep=lambda s: None)
    assert r["state"] == "ok" and len(calls) == 2


def repo(body, status=200):
    return lambda path: (status, body)


def test_repo_states():
    c = lambda body, status=200: h.check_repo("o/r", getter=repo(body, status), today=TODAY)
    assert c({}, 404)["state"] == "missing"
    assert c({"archived": True, "full_name": "o/r"})["state"] == "archived"
    assert c({"full_name": "o/new", "pushed_at": "2026-11-01T00:00:00Z"})["state"] == "renamed"
    assert c({"full_name": "o/r", "pushed_at": "2025-01-01T00:00:00Z"})["state"] == "quiet"
    assert c({"full_name": "o/r", "pushed_at": "2026-11-01T00:00:00Z"})["state"] == "ok"
    assert c({}, 403)["state"] == "unknown"


def test_run_and_render():
    tools = [
        {"id": "good", "name": "Good", "links": [{"label": "g", "url": "https://good.example/"}], "verified": {"date": "2026-11-01"}},
        {"id": "dead", "name": "Dead", "links": [{"label": "d", "url": "https://dead.example/"}], "github": "o/r", "verified": {"date": "2026-11-01"}},
        {"id": "old", "name": "Old", "links": [], "verified": {"date": "2026-01-01"}},
    ]
    results = h.run(
        tools,
        url_checker=lambda u: {"url": u, "state": "ok" if "good" in u else "dead", "why": "HTTP 404"},
        repo_checker=lambda r: {"repo": r, "state": "archived", "why": "repository is archived"},
        today=TODAY, workers=2)
    by = {r["id"]: r for r in results}
    assert by["good"]["findings"] == []
    states = {f[0] for f in by["dead"]["findings"]}
    assert states == {"dead", "archived"}
    assert [f[0] for f in by["old"]["findings"]] == ["reverify"]
    text = h.render(results, today=TODAY)
    assert "3 tools checked, 2 with findings (3 in total)" in text
    assert h.count_findings(results) == 3
