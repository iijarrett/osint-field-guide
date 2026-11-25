<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You suspect a fake — AI-generated or manipulated media](13-synthetic-media.md) · [Index](../README.md) · [Skip — and why →](15-skip.md)

# 14. Cross-cutting: tradecraft, capture & analysis

The layer that sits over all the sections above — what you set up before you start, how you record what you find, how you turn findings into an argument, and how to keep watching once the one-off search is done. Worth reading last and using from the first minute.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Capture discipline — the habit, then the tool](#capture) | `START` | free · practice |
| [ArchiveBox](#archivebox) | `DEEPER` | free · local tool · Python / Docker |
| [SingleFile](#singlefile) | `START` | free · browser extension + CLI |
| [ArchiveWeb.page & Browsertrix (Webrecorder)](#webrecorder) | `DEEPER` | free tool · hosted option |
| [Hunchly](#hunchly) | `GATED` | paid · browser extension |
| [Maltego Community Edition](#maltego-osint) | `DEEPER` | free account · local tool |
| [SpiderFoot](#spiderfoot) | `DEEPER` | free · local tool · slowing |
| [recon-ng](#reconng) | `DEEPER` | free · local tool · dormant |
| [Bellingcat's Online Investigation Toolkit](#directories) | `START` | free · site |
| [A research identity that survives contact](#sockpuppet) | `DEEPER` | free · practice · slow |
| [Build the timeline — where analysis starts](#timeline) | `START` | free · practice |
| [Verification — before you believe it](#verification) | `START` | free · practice |
| [From one-off search to standing collection](#monitoring) | `DEEPER` | free · sites + scripts |
| [MITRE ATT&CK, MISP & OpenCTI](#standing-intel) | `DEEPER` | free · site + Docker |
| [The Berkeley Protocol](#berkeley-protocol) | `START` | free · reading |
| [Trace Labs Search Party](#trace-labs) | `START` | free · practice · community event |

<a id="capture"></a>
### Capture discipline — the habit, then the tool
`START` · free · practice

Every finding gets four things recorded at the moment you find it: the **full URL**, the **UTC timestamp**, a **screenshot showing the URL bar**, and an **archive link**. Keep a running log — a plain markdown file or an Obsidian vault is entirely sufficient — with one entry per finding and an explicit note of which selector it came from.

*Why it's item one here:* an investigation you can't reconstruct is worthless, and pages disappear precisely when they matter. This also forces the discipline of separating *what you observed* from *what you concluded* — the distinction that keeps an OSINT report honest.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="archivebox"></a>
### ArchiveBox
`DEEPER` · free · local tool · Python / Docker

A self-hosted web archiver. Feed it URLs and it saves each page several ways — HTML, a PDF, a screenshot, a WARC, the media — into a folder you own, with a web UI to browse them.

*Why it beats "screenshot it":* you get a copy that's searchable, hashed and independent of whether the Wayback Machine happened to capture the page. It's the free, scriptable stand-in for Hunchly's capture, and it can ingest a whole list of URLs from your case log in one command. Upstream describes Docker Compose as its recommended install.

**Install and run**

```sh
# Docker
docker run -v $PWD/archive:/data -p 8000:8000 -it archivebox/archivebox init --setup
#   (then run it the same way with 'server')
# Linux/Mac
pipx install archivebox ; archivebox init ; archivebox add 'https://example.com'
# Windows: use the Docker line, or run the Linux line inside WSL — upstream lists no native Windows install
```

Upstream's page was read on 23 Nov 2026 and describes active development; the Homebrew formula the guide expected does not exist, so it isn't listed. The Docker image tag and flags follow the project's documented pattern — confirm against its README before relying on them.

**Links:** [example.com](https://example.com)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="singlefile"></a>
### SingleFile
`START` · free · browser extension + CLI

A browser extension that saves the page you're looking at into one self-contained HTML file — styles, images and all — in a single click. Available for Chrome, Firefox, Edge and Safari, and as a command-line tool for scripted capture.

*Why it's the capture you'll actually use:* it works on logged-in and JavaScript-heavy pages that a URL-based archiver can't reach, and one file is easy to hash and file under `capture/`. Use it for what's on your screen, ArchiveBox for what you can fetch by address.

**Install and run**

```sh
# All OS: install from the Chrome Web Store, Firefox Add-ons or Edge Add-ons page for 'SingleFile'
# CLI
npm install -g single-file-cli
#   then single-file <url> out.html
```

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="webrecorder"></a>
### ArchiveWeb.page & Browsertrix (Webrecorder)
`DEEPER` · free tool · hosted option

Webrecorder's tools capture the web the way a browser actually experienced it. **ArchiveWeb.page** (a Chrome extension or desktop app) records everything you click through into a replayable file; **ReplayWeb.page** plays those files back; **Browsertrix** automates the same thing at scale, with a hosted paid service.

*Why it's the heavyweight option:* it preserves interaction — a scrolling feed, a map you panned — in a standard archive format (WACZ) you can keep and re-open years later. For a single static page SingleFile is quicker; for a social feed or an interactive page this is the tool.

[webrecorder.net](https://webrecorder.net/) — ArchiveWeb.page from the Chrome Web Store or as a desktop app · Browsertrix is a hosted service with a free trial

<sub>Last reviewed 2026-11-23</sub>

---

<a id="hunchly"></a>
### Hunchly
`GATED` · paid · browser extension

Automates the above. Turn it on at the start of a case and it silently captures every page you visit — full content, screenshot, hash, timestamp — into a case file, tracks your selectors, highlights them across pages, and exports a report. Built specifically for investigators who may have to defend their evidence.

*Why it's the professional standard:* it removes the single biggest failure mode, which is forgetting to capture something. **Maltego acquired Hunchly in May 2025**, so expect tighter integration with Maltego graphs over time — worth factoring in if you're choosing a long-term workflow. Subscription-priced — the Classic licence (local storage) is listed at €149 or $169 a year as of November 2026, with a 30-day free trial, and the site now carries Maltego Technologies' name; the free capture habit above is the honest substitute until the work justifies it.

[hunch.ly](https://www.hunch.ly/) — free trial available

<sub>Last reviewed 2026-11-23</sub>

---

<a id="maltego-osint"></a>
### Maltego Community Edition
`DEEPER` · free account · local tool

Link analysis — the visual, graph-based way of doing everything on this guide. Drop an entity on the canvas, run a Transform, and it fans out into related entities: domain to subdomains to IPs to certificates to owners. The graph is the point; connections nobody was looking for become visible.

*Current CE limits, September 2026:* free with a Maltego ID, up to **10,000 entities per graph** but only **24 results per Transform**, with a baseline of 200 credits a month. That cap makes CE a learning tool rather than a production one — which is genuinely fine, because the skill it teaches is thinking in graphs. Maltego's own pricing page confirms the free Basic plan and its 200 monthly credits; the entity and result caps above are as last checked in September, so re-verify them before quoting.

**Install and run**

```sh
# Windows: download the installer from maltego.com/downloads
# macOS
brew install --cask maltego
# Linux: preinstalled on Kali — or the .deb from maltego.com/downloads
```

Needs the free Maltego ID either way.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="spiderfoot"></a>
### SpiderFoot
`DEEPER` · free · local tool · slowing

Automated OSINT at scale. Point it at a domain, IP, email, name or phone number, pick your modules, and it queries 200+ data sources and correlates everything into a browsable result set with a web UI. The most complete "press go" OSINT automation that's free.

*Know the status before you commit:* **Intel 471 acquired SpiderFoot in late 2022**, spiderfoot.net now redirects to intel471.com, the commercial SpiderFoot HX folded into their platform, and open-source development has visibly slowed — the tree has sat at v4.0 for some time. It still works and it's still in Kali. Treat it as a capable, stable, no-longer-advancing tool rather than one to build a workflow around.

**Install and run**

```sh
# All OS
git clone https://github.com/smicallef/spiderfoot ; cd spiderfoot ; pip install -r requirements.txt
# Run
python3 sf.py -l 127.0.0.1:5001
#   (then open http://127.0.0.1:5001)
# Kali: already installed
```

Use a virtual environment, and on Windows run it inside WSL — it is built and tested on Linux. Source at github.com/smicallef/spiderfoot.

**Links:** [github.com/smicallef/spiderfoot](https://github.com/smicallef/spiderfoot)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="reconng"></a>
### recon-ng
`DEEPER` · free · local tool · dormant

A reconnaissance framework built on the Metasploit model — a module marketplace, a workspace database, and a console you drive interactively. Install the modules you need, set your API keys once, and the results accumulate in a queryable local database across a whole engagement.

*Honest status:* upstream has been at 5.1.2 and effectively dormant for years, though Kali still repackages it (5.1.2-2 as of late 2025) and it runs fine. The **workspace database is the reason to still use it** — nothing else on this guide accumulates findings across sessions the way it does. Learn it for the model; don't expect new modules.

**Install and run**

```sh
# All OS
git clone https://github.com/lanmaster53/recon-ng ; cd recon-ng ; pip install -r REQUIREMENTS
# Run
python3 recon-ng
# Kali: preinstalled
```

Source at github.com/lanmaster53/recon-ng. Best run on Linux or in WSL.

**Links:** [github.com/lanmaster53/recon-ng](https://github.com/lanmaster53/recon-ng)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="directories"></a>
### Bellingcat's Online Investigation Toolkit
`START` · free · site

The curated directory to keep bookmarked — several hundred tools sorted by task and region, each with a note on what it actually does, maintained by people who use them on real investigations. Covers the long tail this guide deliberately doesn't: satellite imagery, maritime and flight tracking, regional registries, archived TV.

*Why this one specifically:* the venerable *OSINT Framework* mind-map that every tutorial links to has aged badly and is full of dead links and defunct services. Bellingcat's toolkit is actively curated and honest about what's broken. When you need a tool for a target type this guide doesn't cover, look here first.

[bellingcat.gitbook.io/toolkit](https://bellingcat.gitbook.io/toolkit)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="sockpuppet"></a>
### A research identity that survives contact
`DEEPER` · free · practice · slow

Several sections here need an account — viewing a LinkedIn profile, joining a Telegram channel, reading a forum. That account must not be yours, and a blank one created this morning gets flagged or banned immediately. A usable research identity needs: an **aged** account with ordinary activity behind it, a profile photo that **does not reverse-image-search** (not a stock photo, not a real person's), a consistent and boring backstory, its own email and number, and its own browser profile or VM that never touches your real accounts.

*Why "aged" is the hard requirement:* platform trust-and-safety weights account age and behavioural history heavily, so the time to create these is **months before you need them** — an identity built the day you need it is the one that gets locked mid-investigation.

> **Check the rules before the tradecraft.** A fake account breaches the terms of service of nearly every platform, which can mean a permanent ban and, in some jurisdictions and some professional contexts, worse. Some engagements explicitly forbid it. Never use one to *interact* — friending, messaging, or joining a private space is a different act from reading — and never impersonate a real person or organization.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="timeline"></a>
### Build the timeline — where analysis starts
`START` · free · practice

Put every dated finding into one chronological table: timestamp (in **UTC**), what happened, the source it came from, and your confidence in it. Domain registered. Account created. First post. Token deployed. Funds moved. Site archived.

*Why it's the step that turns collection into a conclusion:* a pile of facts proves nothing; the same facts in order show *sequence*, and sequence is the argument. It also exposes your gaps and your contradictions faster than rereading notes — two sources disagreeing about a date is visible instantly in a timeline and invisible in a folder. Keep **observation and inference in separate columns**; a plain markdown table or spreadsheet is entirely sufficient.

Mind the timezones: normalize everything to UTC as you record it, and note the original zone — a "same day" that's actually two days apart has broken more findings than any tool failure

<sub>Last reviewed 2026-11-23</sub>

---

<a id="verification"></a>
### Verification — before you believe it
`START` · free · practice

The discipline for a claim, an image, or a source you're about to rely on. For **media**: find the earliest version (TinEye sorted oldest-first, [§07](07-photo-video.md)), establish where and when it was actually taken, and check whether it's real footage being recycled from an older event — the most common form of false claim by far. For a **source**: who owns the outlet, does it publish corrections, does it have a named masthead, and does any independent outlet carry the same story.

*Why it's a cross-cutting item and not a section:* it applies to everything above. The reflex worth building is **"what would make this false?"** asked before you add a finding to the timeline rather than after you publish it. Lateral reading — leaving the page to check the claim elsewhere — beats scrutinizing the page itself, every time. The **absence** of corroboration is itself a finding worth recording.

Media Bias/Fact Check and Wikipedia's article on the outlet for ownership and track record · [Bellingcat's case write-ups](https://www.bellingcat.com/category/resources/) are the best free training in how the reasoning actually goes

<sub>Last reviewed 2026-11-23</sub>

---

<a id="monitoring"></a>
### From one-off search to standing collection
`DEEPER` · free · sites + scripts

Most of this guide answers a question once. Monitoring answers it continuously. The free layer goes a long way: **Google Alerts** for a name or phrase, **RSS** off anything that still publishes a feed, **crt.sh** polled for newly issued certificates on your domain and its typosquats, **Have I Been Pwned domain monitoring**, GitHub's own secret-scanning alerts, and a scheduled script hitting the APIs from [§05](05-domain-ip-network.md) into a log you diff.

*Why the certificate feed is the one to set up first:* it tells you a lookalike domain exists the day it's certified, usually days before any phishing email goes out — the earliest warning available and it's free. **Tune ruthlessly:** a monitoring system that cries wolf gets ignored within a fortnight, which is worse than not having it. Start with two or three high-signal queries and add only what earns its place.

Google Alerts · [crt.sh](https://crt.sh/) RSS · [HIBP domain monitoring](https://haveibeenpwned.com/DomainSearch) · a cron job and a diff covers the rest

<sub>Last reviewed 2026-11-23</sub>

---

<a id="standing-intel"></a>
### MITRE ATT&CK, MISP & OpenCTI
`DEEPER` · free · site + Docker

Where indicators go once you have them. **MITRE ATT&CK** is the shared vocabulary for how attackers behave, so your report says "credential dumping" in terms everyone maps identically. **MISP** and **OpenCTI** are open-source platforms for storing, linking and sharing indicators, both usually run in Docker.

*Why a defender's guide needs them:* an investigation produces domains, hashes and IPs, and a platform gives them structure and a format (STIX) other tools and teams can consume. The learning curve is steep, so stand one up locally for practice rather than meeting it for the first time on a job.

[attack.mitre.org](https://attack.mitre.org/) · [misp-project.org](https://www.misp-project.org/) · [github.com/OpenCTI-Platform/opencti](https://github.com/OpenCTI-Platform/opencti) — follow each project's own Docker deployment docs; not scripted here

<sub>Last reviewed 2026-11-23</sub>

---

<a id="berkeley-protocol"></a>
### The Berkeley Protocol
`START` · free · reading

The UN human rights office's professional standard for digital open-source investigations, written with the Human Rights Center at UC Berkeley. It sets out how to plan, collect, preserve, verify and analyze online material so that it holds up in a legal or human-rights setting.

*Why it's on a technical guide:* it names the method this whole guide is a toolbox for, in language a court or an employer recognizes. Mapping your own loop ([§00](00-bench-and-loop.md)) to its six stages — online inquiry, preliminary assessment, collection, preservation, verification, investigative analysis — is the quickest way to make a writeup read as professional.

[ohchr.org — Berkeley Protocol](https://www.ohchr.org/en/publications/policy-and-methodological-publications/berkeley-protocol-digital-open-source) — the page refuses automated fetching, so open it in a browser

<sub>Last reviewed 2026-11-23</sub>

---

<a id="trace-labs"></a>
### Trace Labs Search Party
`START` · free · practice · community event

A crowdsourced OSINT event where teams gather public information to help locate missing persons, under strict rules, with the results handed to law enforcement. Trace Labs describes it as OSINT only — no contact with subjects and no pursuit of suspects.

*Why it's the practice to seek out:* it's real casework with real rules and a scoring system, the closest thing to supervised experience a student can get, and it's the kind of line a hiring manager recognizes. Their page doesn't make the schedule or eligibility clear, so check it for the next event.

[tracelabs.org/initiatives/search-party](https://www.tracelabs.org/initiatives/search-party) — sign up through their site

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
