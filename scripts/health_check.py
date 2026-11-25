#!/usr/bin/env python3
"""Check every link and GitHub repository in data/tools.yml and write a report.

    python scripts/health_check.py                      print the report
    python scripts/health_check.py --report out.md      also write it to a file
    python scripts/health_check.py --strict             exit 1 if anything needs action
    python scripts/health_check.py --only maigret,amass check selected tool ids

Findings (these need a human):
    dead        link returns 404/410, or the host no longer resolves, or it keeps failing
    moved       link redirects to a different registered domain
    archived    GitHub repository is archived
    missing     GitHub repository returns 404
    renamed     GitHub repository was renamed or transferred
    quiet       GitHub repository has had no push for more than a year (skipped when the entry's kind
                says stale, dormant or slowing: it already says so)
    reverify    the entry's review date is older than the limit

Not findings: sites that answer 401/403/429 to automated requests are reported as "unknown"
because many legitimate OSINT sites block bots. Set GITHUB_TOKEN to raise the GitHub API limit.

Only the standard library and PyYAML are used.
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

from osintlib import load, load_ignore, real_tools

UA = "Mozilla/5.0 (compatible; osint-field-guide-health/1.0; +https://github.com/iijarrett/osint-field-guide)"
BOT_BLOCKED = {401, 403, 405, 406, 429, 451, 503, 999}
TRANSIENT = {0, 502, 504}
STALE_WORDS = re.compile(r"stale|dormant|slowing")
QUIET_DAYS = 365
REVERIFY_DAYS = 180


def registered_domain(host):
    """Last two labels, or three for common two-part public suffixes. Good enough to spot a domain change."""
    host = (host or "").lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in ("co", "com", "org", "gov", "ac") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def fetch(url, method="GET", timeout=15):
    """Return (status, final_url). status is 0 on a network failure; final_url is None then."""
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.geturl() if hasattr(e, "geturl") else url
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError, OSError):
        return 0, None


def check_url(url, fetcher=fetch, retries=2, sleep=time.sleep):
    """Classify one URL. Returns dict(url, state, status, final)."""
    status, final = 0, None
    for attempt in range(retries + 1):
        status, final = fetcher(url, "GET")
        if status in TRANSIENT and attempt < retries:
            sleep(1.5 * (attempt + 1))
            continue
        break
    if status == 0:
        return {"url": url, "state": "dead", "status": 0, "final": None, "why": "no response (DNS, TLS or connection failure)"}
    if status in (404, 410):
        return {"url": url, "state": "dead", "status": status, "final": final, "why": "HTTP %d" % status}
    if status >= 500 and status not in BOT_BLOCKED:
        return {"url": url, "state": "dead", "status": status, "final": final, "why": "HTTP %d" % status}
    if status in BOT_BLOCKED:
        return {"url": url, "state": "unknown", "status": status, "final": final, "why": "answers automated requests with HTTP %d" % status}
    if final and registered_domain(urlparse(final).hostname) != registered_domain(urlparse(url).hostname):
        return {"url": url, "state": "moved", "status": status, "final": final, "why": "redirects to %s" % final}
    return {"url": url, "state": "ok", "status": status, "final": final, "why": ""}


def github_get(path, token=None, timeout=20):
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request("https://api.github.com" + path, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf8"))
        except Exception:
            body = {}
        return e.code, body
    except (urllib.error.URLError, socket.timeout, OSError):
        return 0, {}


def check_repo(repo, getter=github_get, today=None):
    """Classify one GitHub repo. Returns dict(repo, state, why)."""
    today = today or datetime.date.today()
    status, body = getter("/repos/" + repo)
    if status == 404:
        return {"repo": repo, "state": "missing", "why": "repository not found"}
    if status in (403, 429):
        return {"repo": repo, "state": "unknown", "why": "GitHub API rate limit (set GITHUB_TOKEN)"}
    if status != 200:
        return {"repo": repo, "state": "unknown", "why": "GitHub API status %s" % status}
    if body.get("archived"):
        return {"repo": repo, "state": "archived", "why": "repository is archived"}
    full = body.get("full_name", repo)
    if full.lower() != repo.lower():
        return {"repo": repo, "state": "renamed", "why": "now %s" % full}
    pushed = body.get("pushed_at")
    if pushed:
        d = datetime.date.fromisoformat(pushed[:10])
        age = (today - d).days
        if age > QUIET_DAYS:
            return {"repo": repo, "state": "quiet", "why": "last push %s (%d days ago)" % (pushed[:10], age)}
    return {"repo": repo, "state": "ok", "why": ""}


def review_age(tool, today=None):
    today = today or datetime.date.today()
    v = tool.get("verified") or {}
    try:
        d = datetime.date.fromisoformat(str(v.get("date")))
    except (TypeError, ValueError):
        return None
    return (today - d).days


def accepted_reason(url, ignore, today):
    """Reason text if this URL is an accepted exception that has not expired, else None."""
    for row in ignore or []:
        if row.get("url") == url:
            try:
                if datetime.date.fromisoformat(str(row.get("until"))) >= today:
                    return "%s (accepted until %s)" % (row.get("reason", ""), row["until"])
            except ValueError:
                return None
    return None


def run(tools, url_checker=check_url, repo_checker=check_repo, today=None, workers=8, ignore=None):
    """Check every tool. Returns a list of per-tool results."""
    today = today or datetime.date.today()
    urls = sorted({l["url"] for t in tools for l in t.get("links", []) or []})
    repos = sorted({t["github"] for t in tools if t.get("github")})
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        url_res = dict(zip(urls, ex.map(url_checker, urls)))
        repo_res = dict(zip(repos, ex.map(repo_checker, repos)))
    results = []
    for t in tools:
        findings, unknown, accepted = [], [], []
        for l in t.get("links", []) or []:
            r = url_res[l["url"]]
            if r["state"] in ("dead", "moved"):
                reason = accepted_reason(l["url"], ignore, today)
                if reason:
                    accepted.append((l["url"], "%s; %s" % (r["why"], reason)))
                else:
                    findings.append((r["state"], l["url"], r["why"]))
            elif r["state"] == "unknown":
                unknown.append((l["url"], r["why"]))
        if t.get("github"):
            r = repo_res[t["github"]]
            if r["state"] == "quiet" and STALE_WORDS.search(t.get("kind", "")):
                pass  # the entry already says plainly that the project is stale or dormant
            elif r["state"] in ("missing", "archived", "renamed", "quiet"):
                findings.append((r["state"], "github.com/" + t["github"], r["why"]))
            elif r["state"] == "unknown":
                unknown.append(("github.com/" + t["github"], r["why"]))
        age = review_age(t, today)
        if age is not None and age > REVERIFY_DAYS and not t.get("step"):
            findings.append(("reverify", t["id"], "last reviewed %d days ago" % age))
        results.append({"id": t["id"], "name": t["name"], "findings": findings, "unknown": unknown, "accepted": accepted})
    return results


def render(results, today=None):
    today = today or datetime.date.today()
    bad = [r for r in results if r["findings"]]
    unk = sum(len(r["unknown"]) for r in results)
    n_find = sum(len(r["findings"]) for r in results)
    out = ["# Tool health report", "", "Checked %s: %d tools checked, %d with findings (%d in total), %d links could not be judged automatically."
           % (today.isoformat(), len(results), len(bad), n_find, unk), ""]
    if not bad:
        out += ["No dead links, moved domains, archived repositories or stale reviews.", ""]
    else:
        out += ["| Tool | Finding | Detail |", "|---|---|---|"]
        for r in bad:
            for state, target, why in r["findings"]:
                out.append("| `%s` | **%s** | %s: %s |" % (r["id"], state, target.replace("|", "\\|"), why))
        out.append("")
    if unk:
        out += ["<details><summary>Links that block automated requests (%d)</summary>" % unk, ""]
        for r in results:
            for target, why in r["unknown"]:
                out.append("- `%s`: %s (%s)" % (r["id"], target, why))
        out += ["", "</details>", ""]
    acc = [(r["id"], u, why) for r in results for u, why in r.get("accepted", [])]
    if acc:
        out += ["<details><summary>Accepted exceptions (%d)</summary>" % len(acc), ""]
        for tid, u, why in acc:
            out.append("- `%s`: %s (%s)" % (tid, u, why))
        out += ["", "</details>", ""]
    out.append("Findings need a human: confirm the change, then update `data/tools.yml` and the entry's review date.")
    return "\n".join(out) + "\n"


def count_findings(results):
    return sum(len(r["findings"]) for r in results)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", help="write the Markdown report to this file")
    ap.add_argument("--strict", action="store_true", help="exit 1 if there are findings")
    ap.add_argument("--only", help="comma-separated tool ids")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv)
    _, tools, _ = load()
    tools = real_tools(tools)
    if args.only:
        want = set(args.only.split(","))
        tools = [t for t in tools if t["id"] in want]
    token = os.environ.get("GITHUB_TOKEN")
    results = run(tools, repo_checker=lambda r: check_repo(r, getter=lambda p: github_get(p, token)),
                  workers=args.workers, ignore=load_ignore())
    text = render(results)
    print(text)
    if args.report:
        with open(args.report, "w", encoding="utf8") as f:
            f.write(text)
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf8") as f:
            f.write("findings=%d\n" % count_findings(results))
    return 1 if (args.strict and count_findings(results)) else 0


if __name__ == "__main__":
    sys.exit(main())
