<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[Index](../README.md) · [You have a username →](01-username.md)

# 00. Before you start: the bench and the loop

Everything below the loop is the toolbox for steps 3 to 5. Install lines assume Windows 11 (PowerShell), macOS (Homebrew) and Debian, Ubuntu or Kali. **Homebrew and PyPI names were checked against their registries on 23 Nov 2026; winget IDs and apt names were not** — if one fails, `winget search <name>` or `apt search <name>` finds the current one, and a row that says "All OS" is the same command on all three.

| Tool | Tier | Cost and kind |
|---|---|---|
| [A research VM or a clean browser profile](#bench-vm) | `DEEPER` | free · practice · one-time |
| [Shared prerequisites: Python, pipx, Go, Git, Docker](#bench-tools) | `DEEPER` | free · local tools · one-time |
| [A key vault and one login per research identity](#bench-keys) | `START` | free · local tool |
| [A case folder and a log, the same every time](#bench-case) | `START` | free · practice |
| [Check what the other side can see, once](#bench-leaks) | `START` | free · site |
| [1 · Scope and authorize](#loop-scope) |  | before the first query |
| [2 · List your seeds, pick a starting section](#loop-seeds) |  | minutes |
| [3 · Collect passive first](#loop-collect) |  | default mode |
| [4 · Capture as you go](#loop-capture) |  | every finding |
| [5 · Pivot, then re-seed](#loop-pivot) |  | the actual skill |
| [6 · Verify before it counts](#loop-verify) |  | gate |
| [7 · Analyze and write up](#loop-report) |  | the deliverable |

<a id="bench-vm"></a>
### A research VM or a clean browser profile
`DEEPER` · free · practice · one-time

A disposable machine — a Kali or Ubuntu VM you can snapshot and throw away — or, at the very least, a separate browser profile that never signs in to anything personal. Every tool on this guide runs from here.

*Why first:* a snapshot means a misbehaving tool costs you a revert instead of a reinstall, and nothing you touch can be tied back to your real accounts.

**Install and run**

```sh
# Windows
winget install Oracle.VirtualBox
# macOS
brew install --cask utm
#   (Apple silicon) or brew install --cask virtualbox (Intel)
# Linux
sudo apt install virtualbox
# Then: import a Kali VM image from kali.org/get-kali, take a snapshot, work from the copy
# Profile
firefox -P
#   (profile manager — make one profile per research identity)
```

Windows and apt names were not machine-checked; Homebrew names were. If one fails, `winget search virtualbox` or `apt search virtualbox` gives the current name.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="bench-tools"></a>
### Shared prerequisites: Python, pipx, Go, Git, Docker
`DEEPER` · free · local tools · one-time

Almost every local tool in this guide installs through one of four routes: `pipx` for Python tools, `go install` for Go tools, `git clone` for projects that ship as source, and Docker for anything with a web service. Set all four up once and the per-tool lines below become one-liners.

*Why pipx and not pip:* it puts each tool in its own isolated environment, so one tool's dependencies can't break another's and nothing touches your system Python. **uv** is the fast installer a few newer tools (theHarvester) now expect.

**Install and run**

```sh
# Windows
winget install Python.Python.3.13 GoLang.Go Git.Git Docker.DockerDesktop
py -m pip install --user pipx ; py -m pipx ensurepath
# macOS
brew install python pipx go git uv ; brew install --cask docker-desktop ; pipx ensurepath
# Linux
sudo apt install python3 pipx golang-go git docker.io ; pipx ensurepath
# All OS
pipx install uv
#   (skip on macOS if you used brew above)
# Check
python --version ; pipx --version ; go version ; git --version ; docker --version
```

Open a new terminal after `pipx ensurepath`. Go tools need a recent Go — subfinder's README asks for 1.24 and httpx's for 1.25 — and the distro `golang-go` is often older; if `go version` is too low, take the tarball from go.dev/dl. Docker Desktop on Windows needs virtualization enabled in firmware.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="bench-keys"></a>
### A key vault and one login per research identity
`START` · free · local tool

API keys, throwaway-account logins and recovery codes live in a password manager, one entry per service and one folder per research identity — never in a text file beside your notes.

*Why it's a step:* OSINT piles up accounts (Shodan, urlscan, VirusTotal, Netlas, a burner Google account for GHunt) and keys. Set them through each tool's config file or an environment variable, and never commit them — a notes repo with a pasted key in it is exactly the mistake [§10](10-code-and-apps.md) exists to catch.

**Install and run**

```sh
# Windows
winget install KeePassXCTeam.KeePassXC
# macOS
brew install --cask keepassxc
# Linux
sudo apt install keepassxc
```

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="bench-case"></a>
### A case folder and a log, the same every time
`START` · free · practice

One folder per investigation with a fixed layout: `capture/` for screenshots and archived pages, `notes/` for the running log, `exports/` for raw tool output, `timeline/` for the table you build in [§14](14-tradecraft-and-analysis.md). One log line per finding.

*Why fixed:* a layout you never have to think about is one you'll actually use at 2 a.m., and it's what lets you hand the folder to someone else. Hash anything you might later have to defend, at the moment you save it.

**Install and run**

```sh
# Windows
New-Item -ItemType Directory -Path case-001\capture, case-001\notes, case-001\exports, case-001\timeline
# macOS/Linux
mkdir -p case-001/{capture,notes,exports,timeline}
# Hash: Win
Get-FileHash -Algorithm SHA256 .\case-001\capture\*
# Hash: Mac
shasum -a 256 case-001/capture/*
# Hash: Linux
sha256sum case-001/capture/*
```

log line: `time (UTC) · selector · source URL · what I saw · confidence · archive link`

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="bench-leaks"></a>
### Check what the other side can see, once
`START` · free · site

Before the first case, load a leak-test page from the bench and confirm the exit IP, DNS resolver and WebRTC address are the ones you expect, and that no personal account is signed in to the browser profile.

*Why:* the bench only protects you if it isn't quietly announcing your home connection. It takes two minutes and is worth repeating after any VPN or network change.

[browserleaks.com](https://browserleaks.com/) — IP, WebRTC and DNS tests

<sub>Last reviewed 2026-11-23</sub>

---

<a id="loop-scope"></a>
### 1 · Scope and authorize
before the first query

Write down who or what you're investigating, why, what you will and won't touch, and who authorized it. For a self-audit the authorization is you; for anyone else it's a written scope.

*Why first:* it's the one step that can't be done afterwards, and it decides which sections are in play. Authorized recon on your own domains can go active; research on a private individual stays strictly passive and may need a lawful basis.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="loop-seeds"></a>
### 2 · List your seeds, pick a starting section
minutes

A seed is whatever you already hold. Write each one down and route it: username → [§01](01-username.md) · email → [§02](02-email.md) · phone → [§03](03-phone.md) · real name → [§04](04-real-name.md) · domain or IP → [§05](05-domain-ip-network.md) · company → [§06](06-organization.md) · image or video → [§07](07-photo-video.md) · social post → [§08](08-social.md) · breach question → [§09](09-breach-credentials.md) · repo or app → [§10](10-code-and-apps.md) · wallet → [§11](11-wallets-tokens.md) · ship, aircraft or satellite image → [§12](12-tracking.md) · suspected fake → [§13](13-synthetic-media.md).

*Why a list:* it turns "look into this" into a queue with an order, and the list is what you extend when a finding becomes a new selector.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="loop-collect"></a>
### 3 · Collect passive first
default mode

Start with sources that never touch the target — certificate logs, archives, public records, search operators, aggregator sites. Treat anything active (scans, brute-forcing, joining a channel, saving a contact) as a separate decision that you log.

*Why:* passive work is invisible and almost always in scope; active work is neither. The `passive`/`active` distinction is the first thing a reviewer of your report will ask about.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="loop-capture"></a>
### 4 · Capture as you go
every finding

URL, UTC timestamp, a screenshot that shows the address bar, and an archive link — recorded when you find it, not at the end. [§14](14-tradecraft-and-analysis.md) covers the habit and the tools (Hunchly, ArchiveBox, SingleFile).

*Why now:* the interesting page is the one that disappears once someone notices attention.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="loop-pivot"></a>
### 5 · Pivot, then re-seed
the actual skill

Every finding is a new selector: a profile gives an email, the email gives a breach, the breach gives a second handle. Add each to the seed list, work it through its own section, and stop when pivots stop paying.

*Why a stop rule:* without one, an investigation expands until it hits the budget. Decide the depth in step 1 — "two hops from the starting selector" is a perfectly good scope.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="loop-verify"></a>
### 6 · Verify before it counts
gate

A finding enters the timeline only after you've asked what would make it false and looked for a second, independent source. One aggregator hit is a lead; a hit confirmed in a primary record is a finding.

*Why a gate:* the cost of a wrong finding grows with every step built on top of it. The method is in [§14](14-tradecraft-and-analysis.md)'s verification entry.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="loop-report"></a>
### 7 · Analyze and write up
the deliverable

Order the dated findings into a timeline (UTC), keep observation and inference in separate columns, then report: the question, scope, method, findings with confidence, what you did *not* do or couldn't verify, and the log as an appendix. Redact third parties.

*Why it's the point:* collection without a report is trivia. A short report that states its limits is more credible than a long one that doesn't.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
