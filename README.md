<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

# OSINT Field Guide

[![Validate](https://github.com/iijarrett/osint-field-guide/actions/workflows/validate.yml/badge.svg)](https://github.com/iijarrett/osint-field-guide/actions/workflows/validate.yml) [![Tool health](https://github.com/iijarrett/osint-field-guide/actions/workflows/health.yml/badge.svg)](https://github.com/iijarrett/osint-field-guide/actions/workflows/health.yml) [![Code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE) [![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey)](LICENSE-CONTENT.md)

**A short list of the best open-source-intelligence tools, organized by what you have in your hand: a username, an email, a photo, a domain, a wallet.** 87 entries, with install lines for Windows, macOS and Linux wherever there is something to install, plain notes on each tool's limits, and a weekly health check that flags dead links and abandoned projects.

## Why this one is different

- **Start from the selector, not the tool.** OSINT is pivoting: one identifier leads to the next. Find the thing you hold in the table below and work that section; each section ends where another begins.
- **A shortlist, not a directory.** Where one tool is clearly the best for the job it is listed alone. A second tool earns a place only when it finds something the first one misses. There is also a [skip list](docs/15-skip.md) of tools that are still recommended elsewhere but are dead, broken or a bad idea.
- **Install lines for three operating systems.** pipx, uv, `go install`, `git clone`, Docker, Homebrew, winget and apt. No piped-to-shell installers; every line is something you can read before you run it.
- **Honest about status.** Each entry carries a review date and says how far its install lines were checked. A scheduled workflow checks every link and every GitHub repository, and opens an issue when something dies, moves or goes quiet for a year.
- **Ethics are part of the entry.** Tools that can hurt people are tagged `GATED`, explained with the legal exposure, and shown with their defensive use. This is a guide for investigators and defenders, not for stalkers.

## Find your starting point

| You have | Go to | Tools |
|---|---|---|
| You have a username | [Section 01](docs/01-username.md) | 4 |
| You have an email address | [Section 02](docs/02-email.md) | 5 |
| You have a phone number | [Section 03](docs/03-phone.md) | 2 |
| You have a real name | [Section 04](docs/04-real-name.md) | 4 |
| You have a domain, IP, or network identifier | [Section 05](docs/05-domain-ip-network.md) | 13 |
| You have a company or organization | [Section 06](docs/06-organization.md) | 6 |
| You have a photo or video | [Section 07](docs/07-photo-video.md) | 5 |
| You have a social account or post | [Section 08](docs/08-social.md) | 6 |
| You want breach & credential exposure | [Section 09](docs/09-breach-credentials.md) | 3 |
| You have source code, a repo, or an app | [Section 10](docs/10-code-and-apps.md) | 4 |
| You have a wallet address or a token | [Section 11](docs/11-wallets-tokens.md) | 3 |
| You have a ship, an aircraft, or a place seen from above | [Section 12](docs/12-tracking.md) | 5 |
| You suspect a fake — AI-generated or manipulated media | [Section 13](docs/13-synthetic-media.md) | 6 |
| **Cross-cutting:** tradecraft, capture and analysis | [Section 14](docs/14-tradecraft-and-analysis.md) | 16 |

**New to this?** Read [Section 00: Before you start: the bench and the loop](docs/00-bench-and-loop.md) first. It covers the research machine, the case folder and the seven-step loop every investigation follows. Install lines assume Windows 11 (PowerShell, winget), macOS (Homebrew) and Debian, Ubuntu or Kali (apt). A row labelled All OS is the same command everywhere.

## How to read an entry

| Tag | Meaning |
|---|---|
| `START` | Free, fast, no setup worth mentioning. The first thing to reach for in that section (41 tools). |
| `DEEPER` | More setup: an install, API keys, a free account or patience. Where the real results usually are. |
| `GATED` | Costs money, needs a business email, or carries real ethical or legal weight (8 tools). Know it exists; think before you reach. |

The *kind* line under each name says whether something is a site (nothing to install), a local tool, or paid. Most OSINT is websites, so most entries have nothing to install.

**Method and ethics.** How the guide's loop lines up with the Berkeley Protocol, where it is thin, and what is gated and why: [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

**Pivot map.** Pick what you already hold (a username, an email, a photo) and see what you can reach next and which tools get you there. It is one self-contained file: download [docs/pivot-map.html](docs/pivot-map.html) and open it in a browser. The same graph as data is in [docs/pivot-map.json](docs/pivot-map.json).

## Read it from the terminal

The same data is available offline as a small command-line reader. It prints entries, cautions and the install lines for your OS, and **never runs anything**.

```sh
pipx install git+https://github.com/iijarrett/osint-field-guide     # or: pip install .  from a clone
osint-guide search username                    # find entries by word
osint-guide show maigret                       # the full entry, with your OS's install lines
osint-guide install maigret --os macos         # just the commands, ready to copy
osint-guide list --tier gated                  # the entries that carry a caution
```

Add `--json` to any command to pipe the result into your own tools.

## The guide

### 00. [Before you start: the bench and the loop](docs/00-bench-and-loop.md)

| Tool | Tier | What it is for |
|---|---|---|
| [A research VM or a clean browser profile](docs/00-bench-and-loop.md#bench-vm) | `DEEPER` | A disposable VM or a clean browser profile to run everything from. |
| [Shared prerequisites: Python, pipx, Go, Git, Docker](docs/00-bench-and-loop.md#bench-tools) | `DEEPER` | One-time setup of Python, pipx, Go, Git and Docker so every later install is a one-liner. |
| [A key vault and one login per research identity](docs/00-bench-and-loop.md#bench-keys) | `START` | A password manager entry per service and a folder per research identity. |
| [A case folder and a log, the same every time](docs/00-bench-and-loop.md#bench-case) | `START` | One folder and one log per investigation, laid out the same way every time. |
| [Check what the other side can see, once](docs/00-bench-and-loop.md#bench-leaks) | `START` | Confirm the exit IP, DNS resolver and WebRTC address before the first case. |

### 01. [You have a username](docs/01-username.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Maigret](docs/01-username.md#maigret) | `START` | Username search across thousands of sites that also parses each hit into a profile dossier. |
| [Sherlock](docs/01-username.md#sherlock) | `START` | The original username hunter: one handle across 400+ networks, fast and simple. |
| [Blackbird](docs/01-username.md#blackbird) | `START` | Username and email search with PDF and CSV export, built on the WhatsMyName dataset, which is now frozen. |
| [Manual handle pivoting](docs/01-username.md#handle-pivot) | `DEEPER` | Vary the handle by hand (jsmith, j_smith, jsmith88) and search it as a quoted string. |

### 02. [You have an email address](docs/02-email.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Epieos](docs/02-email.md#epieos) | `START` | Email or phone number in, registered services and linked Google account data out. |
| [GHunt](docs/02-email.md#ghunt) | `DEEPER` | Deep extraction from a Google account: name, photo, Maps reviews, YouTube and Calendar. |
| [holehe](docs/02-email.md#holehe) | `DEEPER` | Checks an email against 120-odd sites through their password-recovery flows. Stale: trust hits, not misses. |
| [Hunter.io & email-format guessing](docs/02-email.md#hunterio) | `DEEPER` | Given a domain, the organization's email pattern and the addresses already known. |
| [Reading the headers, not just the address](docs/02-email.md#email-headers) | `START` | Read the full message headers to see where a message really came from and whether SPF, DKIM and DMARC passed. |

### 03. [You have a phone number](docs/03-phone.md)

| Tool | Tier | What it is for |
|---|---|---|
| [PhoneInfoga](docs/03-phone.md#phoneinfoga) | `START` | Country, carrier and line type for a number, then a sweep of public sources. |
| [Messaging-app presence check](docs/03-phone.md#messaging-presence) | `DEEPER` | Save the number on a burner device and see which messaging apps show a profile. |

### 04. [You have a real name](docs/04-real-name.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Search operators, used properly](docs/04-real-name.md#search-operators) | `START` | Quoted phrases, site:, filetype: and friends, which outperform most dedicated tools for a name. |
| [People-search aggregators](docs/04-real-name.md#people-search) | `GATED` | Data-broker profiles: leads to confirm elsewhere, never findings on their own. |
| [Court, property & voter records](docs/04-real-name.md#public-records) | `DEEPER` | Court, property and voter records: the primary sources the aggregators scrape. |
| [Obituaries & genealogy sources](docs/04-real-name.md#genealogy) | `DEEPER` | Obituaries and genealogy sites that name a whole family in one permanent document. |

### 05. [You have a domain, IP, or network identifier](docs/05-domain-ip-network.md)

| Tool | Tier | What it is for |
|---|---|---|
| [WHOIS / RDAP & DNS history](docs/05-domain-ip-network.md#whois-rdap) | `START` | Registration dates, registrar and nameservers, plus historical DNS from before privacy was switched on. |
| [ASN, BGP & netblock lookups](docs/05-domain-ip-network.md#asn-bgp) | `START` | Map an IP to its network block and the autonomous system that runs it. |
| [Certificate transparency logs](docs/05-domain-ip-network.md#crtsh) | `START` | Search the public certificate logs for every subdomain a domain has ever certified. |
| [urlscan.io](docs/05-domain-ip-network.md#urlscan-osint) | `START` | Sandboxed page scans with screenshot and request chain, plus a searchable archive of everyone's scans. |
| [Shodan, Censys & friends](docs/05-domain-ip-network.md#shodan-censys) | `GATED` | Search engines for internet-facing machines: ports, banners, certificates, exposed panels. |
| [LeakIX](docs/05-domain-ip-network.md#leakix) | `DEEPER` | Index of exposed misconfigurations: open databases, buckets, Git directories and admin panels. |
| [GrayhatWarfare — exposed cloud storage](docs/05-domain-ip-network.md#bucket-search) | `DEEPER` | Search engine over publicly readable cloud storage buckets. |
| [OWASP Amass](docs/05-domain-ip-network.md#amass) | `DEEPER` | Deep attack-surface mapping from dozens of passive sources, with optional active modes. |
| [subfinder + httpx](docs/05-domain-ip-network.md#projectdiscovery) | `DEEPER` | subfinder lists subdomains passively; httpx shows which ones answer, with titles and tech. |
| [Wayback Machine & archive.today](docs/05-domain-ip-network.md#wayback) | `START` | Archived copies of what a site used to say, and a way to preserve what it says now. |
| [DNSDumpster, Robtex & DNSViz](docs/05-domain-ip-network.md#dns-browser) | `START` | No-install DNS views: host maps, reverse nameserver and IP pivots, DNSSEC chains. |
| [Indicator enrichment — is this already known bad?](docs/05-domain-ip-network.md#enrichment) | `START` | Check whether an IP, domain, URL or hash is already known bad before investigating from scratch. |
| [WiGLE — geolocating a Wi-Fi network](docs/05-domain-ip-network.md#wigle) | `DEEPER` | Geolocate a Wi-Fi network from its BSSID or SSID in a global wardriving database. |

### 06. [You have a company or organization](docs/06-organization.md)

| Tool | Tier | What it is for |
|---|---|---|
| [OpenCorporates & national registries](docs/06-organization.md#opencorporates) | `START` | Worldwide company registries in one search: officers, incorporation dates and filings. |
| [SEC EDGAR & OCCRP Aleph](docs/06-organization.md#edgar-aleph) | `DEEPER` | EDGAR for US public-company filings; OCCRP Aleph for leaks, sanctions and registries. |
| [OpenSanctions, ICIJ Offshore Leaks & Open Ownership](docs/06-organization.md#sanctions-ownership) | `START` | Beneficial-ownership, sanctions and offshore-leak databases. |
| [theHarvester](docs/06-organization.md#theharvester) | `DEEPER` | Emails, employee names, subdomains and hosts for a domain from search engines and logs. |
| [Tech-stack fingerprinting & job postings](docs/06-organization.md#tech-stack) | `DEEPER` | Fingerprint a site's stack, and read the job postings that list the rest. |
| [Shared tracker & analytics IDs](docs/06-organization.md#tracker-ids) | `DEEPER` | Analytics, AdSense and pixel IDs that link a network of sites to one operator. |

### 07. [You have a photo or video](docs/07-photo-video.md)

| Tool | Tier | What it is for |
|---|---|---|
| [ExifTool — read the metadata first](docs/07-photo-video.md#exif-osint) | `START` | Read embedded metadata first: GPS, timestamps, camera serial numbers, editing software. |
| [Reverse image search — all four engines](docs/07-photo-video.md#reverse-image) | `START` | Yandex, Google Lens, Bing and TinEye each find different things; crop before you search. |
| [Geolocation — the chronolocation toolkit](docs/07-photo-video.md#geolocation) | `DEEPER` | Place and date an unlabelled photo from terrain, signage, shadows and street imagery. |
| [InVID / WeVerify — video verification](docs/07-photo-video.md#invid) | `DEEPER` | Browser extension for video: keyframe extraction, metadata, magnification and forensic filters. |
| [Facial-recognition search engines](docs/07-photo-video.md#face-search) | `GATED` | Search the web by face. The most invasive capability in this guide; use it on yourself only. |

### 08. [You have a social account or post](docs/08-social.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Native platform search, used hard](docs/08-social.md#platform-search) | `START` | Each platform's own advanced search, which is often the only thing that still works. |
| [Mastodon, the Fediverse & Bluesky](docs/08-social.md#fediverse-bluesky) | `DEEPER` | Searching Mastodon, the wider Fediverse and Bluesky, which work differently from closed networks. |
| [Deleted posts & social archives](docs/08-social.md#social-archives) | `START` | Archives and caches that remember what people delete. |
| [Telegram & Discord](docs/08-social.md#telegram-discord) | `DEEPER` | Where much threat-actor activity lives, and how to read it without joining in. |
| [Telling a real account from a fake one](docs/08-social.md#bot-detection) | `DEEPER` | Tell real accounts from fake ones by observable behaviour, not by a bot score. |
| [Dark-web research, safely](docs/08-social.md#darkweb) | `GATED` | Leak-site trackers first, Tor in a disposable VM only if you must. |

### 09. [You want breach & credential exposure](docs/09-breach-credentials.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Have I Been Pwned](docs/09-breach-credentials.md#hibp) | `START` | The ethical breach index: which breaches an address is in, never the passwords. |
| [Commercial breach-data search](docs/09-breach-credentials.md#breach-search) | `GATED` | Paid indexes that return breached records themselves. Powerful, and one subpoena from your worst browser history. |
| [Run this whole guide on yourself](docs/09-breach-credentials.md#self-exposure) | `START` | Run this whole guide against yourself: the best exercise on the list. |

### 10. [You have source code, a repo, or an app](docs/10-code-and-apps.md)

| Tool | Tier | What it is for |
|---|---|---|
| [GitHub code search & dorking](docs/10-code-and-apps.md#github-dorking) | `START` | GitHub code search qualifiers for finding committed secrets and internal naming. |
| [grep.app, Sourcegraph, GitLab & Searchcode](docs/10-code-and-apps.md#code-search-engines) | `DEEPER` | grep.app, Sourcegraph, GitLab and Searchcode reach code GitHub search does not. |
| [TruffleHog](docs/10-code-and-apps.md#secret-scanners) | `DEEPER` | Scan a repo's full history for credentials and test whether they still work. |
| [Pulling intelligence out of a mobile app](docs/10-code-and-apps.md#apk-analysis) | `GATED` | Static analysis of an Android app: endpoints, keys, trackers, permissions, signing details. |

### 11. [You have a wallet address or a token](docs/11-wallets-tokens.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Block explorers — read the ledger directly](docs/11-wallets-tokens.md#block-explorers) | `START` | Read any chain's ledger directly: transactions, counterparties and the first funding source. |
| [Visual tracing & address clustering](docs/11-wallets-tokens.md#chain-tracing) | `DEEPER` | Graph tools that draw fund flows and cluster addresses into entities. |
| [Token & rug-pull checks](docs/11-wallets-tokens.md#rugpull-checks) | `START` | Contract and liquidity checks that tell you whether a token is a trap. |

### 12. [You have a ship, an aircraft, or a place seen from above](docs/12-tracking.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Flightradar24, FlightAware & ADS-B Exchange](docs/12-tracking.md#air-tracking) | `START` | Live and historical aircraft positions from transponder broadcasts. |
| [MarineTraffic, VesselFinder, Equasis & Global Fishing Watch](docs/12-tracking.md#ship-tracking) | `START` | AIS vessel positions plus the registry layer behind them. |
| [Free satellite imagery — Copernicus, NASA Worldview & FIRMS, Google Earth Pro](docs/12-tracking.md#sat-free) | `START` | Free satellite imagery from Copernicus, NASA and similar sources. |
| [High-resolution and radar imagery](docs/12-tracking.md#sat-commercial) | `GATED` | High-resolution and radar imagery you can order: Planet, SkyFi, Umbra. |
| [Reading imagery — date, resolution, shadows, clouds](docs/12-tracking.md#change-detection) | `DEEPER` | Four questions to ask of any overhead image: date, resolution, shadows, what changed. |

### 13. [You suspect a fake — AI-generated or manipulated media](docs/13-synthetic-media.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Check provenance first — Content Credentials (C2PA)](docs/13-synthetic-media.md#c2pa) | `START` | Verify a file's signed Content Credentials; a missing manifest means unknown, not clean. |
| [Vendor watermark checkers — SynthID, OpenAI, Meta](docs/13-synthetic-media.md#watermark-check) | `START` | Vendor checkers for SynthID and similar marks: strong when positive, nearly useless when negative. |
| [AI-image detectors — Hive, AI or Not & friends](docs/13-synthetic-media.md#ai-detectors) | `DEEPER` | AI-image classifiers (Hive, AI or Not): one weak signal, never a finding. |
| [Image forensics — FotoForensics, Forensically & ExifTool](docs/13-synthetic-media.md#image-forensics) | `DEEPER` | Error-level analysis, clone detection and metadata checks for manipulated images. |
| [Face-swap and voice-clone checks](docs/13-synthetic-media.md#deepfake-audio-face) | `DEEPER` | DeepFake-O-Meter and voice-clone detectors; keyframe search and callbacks often beat both. |
| [The two-indicator rule — context beats classifiers](docs/13-synthetic-media.md#two-indicators) | `START` | Call a file synthetic or authentic only on two independent indicators. |

### 14. [Cross-cutting: tradecraft, capture & analysis](docs/14-tradecraft-and-analysis.md)

| Tool | Tier | What it is for |
|---|---|---|
| [Capture discipline — the habit, then the tool](docs/14-tradecraft-and-analysis.md#capture) | `START` | Record URL, UTC time, screenshot and archive link the moment you find something. |
| [ArchiveBox](docs/14-tradecraft-and-analysis.md#archivebox) | `DEEPER` | Self-hosted web archiver that keeps your own copies of pages you cite. |
| [SingleFile](docs/14-tradecraft-and-analysis.md#singlefile) | `START` | Browser extension that saves a page as one self-contained HTML file. |
| [ArchiveWeb.page & Browsertrix (Webrecorder)](docs/14-tradecraft-and-analysis.md#webrecorder) | `DEEPER` | Capture pages and sessions the way a browser actually saw them, with replayable archives. |
| [Hunchly](docs/14-tradecraft-and-analysis.md#hunchly) | `GATED` | Paid browser extension that auto-captures every page of a case with hashes and timestamps. |
| [Maltego Community Edition](docs/14-tradecraft-and-analysis.md#maltego-osint) | `DEEPER` | Graph-based link analysis; the free edition is a learning tool, not a production one. |
| [SpiderFoot](docs/14-tradecraft-and-analysis.md#spiderfoot) | `DEEPER` | Automated OSINT across 200+ sources with a web UI. Stable but no longer advancing. |
| [recon-ng](docs/14-tradecraft-and-analysis.md#reconng) | `DEEPER` | Recon framework with a module marketplace and a workspace database that persists across sessions. |
| [Bellingcat's Online Investigation Toolkit](docs/14-tradecraft-and-analysis.md#directories) | `START` | Bellingcat's curated toolkit directory, for the target types this guide does not cover. |
| [A research identity that survives contact](docs/14-tradecraft-and-analysis.md#sockpuppet) | `DEEPER` | What a usable research identity needs, why it must be aged, and the rules to check first. |
| [Build the timeline — where analysis starts](docs/14-tradecraft-and-analysis.md#timeline) | `START` | One UTC-ordered table of every dated finding, with observation and inference kept apart. |
| [Verification — before you believe it](docs/14-tradecraft-and-analysis.md#verification) | `START` | Ask what would make a claim, image or source false before you rely on it. |
| [From one-off search to standing collection](docs/14-tradecraft-and-analysis.md#monitoring) | `DEEPER` | Standing collection: alerts, certificate feeds and scheduled diffs instead of one-off searches. |
| [MITRE ATT&CK, MISP & OpenCTI](docs/14-tradecraft-and-analysis.md#standing-intel) | `DEEPER` | MITRE ATT&CK, MISP and OpenCTI: where indicators go once you have them. |
| [The Berkeley Protocol](docs/14-tradecraft-and-analysis.md#berkeley-protocol) | `START` | The UN human rights office's standard for digital open-source investigations. |
| [Trace Labs Search Party](docs/14-tradecraft-and-analysis.md#trace-labs) | `START` | Crowdsourced OSINT events that search for missing persons under strict rules. |

### 15. [Skip — and why](docs/15-skip.md)

16 tools and habits that keep getting recommended and shouldn't be. Each has the reason.

## Ground rules

1. **Pivot deliberately.** Each finding is a new selector. The skill is seeing which thread to pull, and stopping when it stops paying.
2. **Corroborate before you conclude.** One aggregator hit is a rumor; a hit confirmed against a primary record is a finding. Keep those two words apart in your notes.
3. **Capture at the moment of discovery.** URL, UTC timestamp, screenshot, archive link. Pages vanish, and the interesting ones vanish fastest.
4. **Know whether you are passive or active.** Reading a certificate log touches nobody. Brute-forcing subdomains or joining a server does. The distinction governs your scope, your legal position and whether the target knows you are there.

**Law and ethics.** Every source in this guide is public, and looking at public information is lawful nearly everywhere. What changes that is who you point it at and what you do next: active reconnaissance without authorization can be unauthorized access; compiling a profile on a private individual without a lawful basis can be harassment or a data-protection offence; and using a credential you found, however you found it, is a crime in essentially every jurisdiction. Professionally the rule is plain: scope in writing, authorization before you start, and a log you would be comfortable handing to a court. "It was all public" describes where the data came from. It says nothing about whether you were entitled to collect it.

OSINT is a research discipline wearing a hacker's clothes. The tools change every year, but pivoting, corroboration, capture and the passive/active line do not.

## Contributing

Tool suggestions, corrections and dead-link reports are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the inclusion bar and how to edit the data; the README and every page under `docs/` are generated from `data/tools.yml`, so edit that file and run `python scripts/build_readme.py`. Security issues: see [SECURITY.md](SECURITY.md).

## License

Code under the [MIT License](LICENSE). Guide text and data under [CC BY 4.0](LICENSE-CONTENT.md). Tool names are trademarks of their owners.
