<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a real name](04-real-name.md) · [Index](../README.md) · [You have a company or organization →](06-organization.md)

# 05. You have a domain, IP, or network identifier

The largest section, and the one that does double duty — this is *both* pre-engagement recon for an assessment and day-to-day threat-intel triage of a phishing domain. Same tools, opposite intent. Watch the passive/active line closely here: several of these touch the target directly.

| Tool | Tier | Cost and kind |
|---|---|---|
| [WHOIS / RDAP & DNS history](#whois-rdap) | `START` | free · site + CLI |
| [ASN, BGP & netblock lookups](#asn-bgp) | `START` | free · sites |
| [Certificate transparency logs](#crtsh) | `START` | free · site |
| [urlscan.io](#urlscan-osint) | `START` | free tier · site + API |
| [Shodan, Censys & friends](#shodan-censys) | `GATED` | free account · paid to use properly |
| [LeakIX](#leakix) | `DEEPER` | free · site + API · account to see detail |
| [GrayhatWarfare — exposed cloud storage](#bucket-search) | `DEEPER` | free tier · site |
| [OWASP Amass](#amass) | `DEEPER` | free · local tool · Go |
| [subfinder + httpx](#projectdiscovery) | `DEEPER` | free · local tools · Go |
| [Wayback Machine & archive.today](#wayback) | `START` | free · sites |
| [DNSDumpster, Robtex & DNSViz](#dns-browser) | `START` | free · sites |
| [Indicator enrichment — is this already known bad?](#enrichment) | `START` | free tier · sites + APIs |
| [WiGLE — geolocating a Wi-Fi network](#wigle) | `DEEPER` | free account · site + API |

<a id="whois-rdap"></a>
### WHOIS / RDAP & DNS history
`START` · free · site + CLI

Registration date, registrar, nameservers, and — occasionally — a real registrant. GDPR redacted most contact details years ago, so the **dates and nameservers** are now the valuable fields. Pair with historical DNS (SecurityTrails, DNSlytics, ViewDNS) to see what the records used to say before privacy was switched on.

*The single best triage signal:* a domain registered four days ago and already sending you email is a phishing domain, and that one field settles it faster than any analysis. Historical records are where the un-redacted 2015 registrant email is still sitting.

`whois example.com` · [viewdns.info](https://viewdns.info/) · [securitytrails.com](https://securitytrails.com/) (free account)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="asn-bgp"></a>
### ASN, BGP & netblock lookups
`START` · free · sites

Every IP belongs to a network block, and every block to an autonomous system (ASN) run by someone. **Hurricane Electric's BGP Toolkit** (bgp.he.net) and **RIPEstat** take an IP, ASN or organization and return the prefixes it announces, its peers, and its registered name and contacts.

*Why it matters:* it answers "what else does this organization run" without touching the target — the netblocks of a company, or the hosting provider behind a phishing site, and which of its neighbours are bulletproof hosts. It's the passive complement to Amass's ASN mapping below.

[bgp.he.net](https://bgp.he.net/) · [stat.ripe.net](https://stat.ripe.net/) · `whois -h whois.cymru.com " -v 203.0.113.5"` for a quick IP-to-ASN lookup on Linux and macOS

<sub>Last reviewed 2026-11-23</sub>

---

<a id="crtsh"></a>
### Certificate transparency logs
`START` · free · site

Every TLS certificate issued by a public CA is written to an append-only public log. Search a domain at **crt.sh** and you get the subdomains it has ever certified — including internal-sounding ones nobody meant to publish: `vpn.`, `staging.`, `jira.`, `backup-admin.`

*Why it's the best free recon there is:* completely passive — you query a log, never the target — and the data is authoritative rather than guessed. It also catches **typosquats and lookalike domains** the moment someone certifies one, which is how you spot a phishing campaign being built against your own org before it launches.

[crt.sh](https://crt.sh/) — try `%.example.com` as the query

<sub>Last reviewed 2026-11-23</sub>

---

<a id="urlscan-osint"></a>
### urlscan.io
`START` · free tier · site + API

Visits a URL in a sandbox on your behalf and hands back a screenshot, the full request chain, every domain contacted, and the page's DOM — without you ever loading it. **Also searchable**: you can hunt the archive of everyone else's scans for a favicon hash, a domain, or a piece of page content.

*Why the search half is underused:* pivoting on a favicon hash or a unique script across urlscan's history finds every other site running the same phishing kit.

[urlscan.io](https://urlscan.io/) — mark sensitive scans **unlisted**; public scans are visible to everyone, including your target

<sub>Last reviewed 2026-11-23</sub>

---

<a id="shodan-censys"></a>
### Shodan, Censys & friends
`GATED` · free account · paid to use properly

Search engines for machines rather than pages. They continuously scan the internet and index what answers — open ports, service banners, software versions, TLS certificates, exposed panels and cameras. Query by organization, ASN, certificate, or product version.

*Current state, November 2026:* Shodan's account page lists a one-time membership at $49 (100 query credits and 16 monitored IPs) with subscription tiers above it, and a free account includes a limited free API plan. **Censys has moved to the Censys Platform and deprecated its Legacy Search and Legacy API**, so older tutorials and scripts point at a dead endpoint; a free Censys account gives basic visibility into standard ports and services. FOFA and ZoomEye are the non-US alternatives with different coverage. **Netlas** has a free community plan — 50 requests a day and 2,500 search results a month, non-commercial — which is currently the more usable free option. **Criminal IP** is live, but its homepage no longer shows a free tier, so check before relying on it. **LeakIX** asks a different question and gets its own entry below.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="leakix"></a>
### LeakIX
`DEEPER` · free · site + API · account to see detail

Shodan tells you *what is running* at an address. LeakIX tells you *what is exposed* — it indexes the misconfigurations themselves: open Elasticsearch and MongoDB instances, world-readable S3 and storage buckets, exposed Git directories, unprotected admin panels, and services matching known vulnerability signatures. Searchable by `port:`, `protocol:`, `asn:` and CIDR range.

*Why it earns a separate entry:* it's a narrower index that answers the question you actually have during an authorized assessment or a self-audit — not "what does this org run" but "what has this org left open." Running your own domains and ASN through it is a five-minute exposure check with a genuinely different result set from Shodan's. It also names the researcher who reported each finding, which makes provenance unusually clear.

[leakix.net](https://leakix.net/) — browsing is open; a free account unlocks the detail on individual findings; the free plan delays results by 15 days and the first paid tier is about €25 a month

> **An open database is still someone's database.** LeakIX shows you unauthenticated services. Connecting to one you don't own is unauthorized access whether or not it asked for a password — the absence of a lock is not an invitation. Look, record, report; never connect.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="bucket-search"></a>
### GrayhatWarfare — exposed cloud storage
`DEEPER` · free tier · site

A search engine over publicly readable cloud storage buckets (S3, Azure and similar). Search by keyword, filename or extension and it lists what was left open — backups, spreadsheets, source archives.

*Why it's here:* misconfigured buckets are one of the commonest self-inflicted exposures, and searching your own organization's names is a fast audit. It sits beside LeakIX above — LeakIX finds exposed services, this finds exposed files.

[grayhatwarfare.com](https://grayhatwarfare.com/) — limited free tier; a paid plan lifts the caps

> **Open is not yours.** A world-readable bucket still belongs to someone. Looking at a listing is research; opening, downloading or modifying someone else's files is unauthorized access. Record the bucket name, report it to its owner, and stop.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="amass"></a>
### OWASP Amass
`DEEPER` · free · local tool · Go

The heavyweight attack-surface mapper. Pulls from dozens of passive sources — certificate logs, search engines, DNS aggregators, ASN data — and optionally goes active with brute-forcing and zone walking, then graphs the whole result. Maps not just subdomains but the netblocks and ASNs an organization owns.

*Why it's the deep option:* nothing else assembles the same breadth in one run, and the ASN mapping finds infrastructure that isn't under the obvious domain at all. **Know which mode you're in** — passive enumeration is invisible, active brute-forcing hammers the target's DNS and will show up in their logs. **Amass is now on v5** (5.1.x), which moved results into a local asset database with an engine service behind the command line, so v4-era tutorials and flags may not apply — read the current docs before copying a command.

**Install and run**

```sh
# macOS
brew install amass
# Linux
sudo apt install amass
#   (Kali and some Debian releases — check the version it gives you)
# Any OS
go install -v github.com/owasp-amass/amass/v5/...@main
#   (needs a current Go; see §00)
```

Upstream's docs live at owasp-amass.github.io/docs. The passive-only flag in v4 was `amass enum -passive -d example.com` — confirm its v5 equivalent there before relying on it.

**Links:** [github.com/owasp-amass/amass](https://github.com/owasp-amass/amass)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="projectdiscovery"></a>
### subfinder + httpx
`DEEPER` · free · local tools · Go

The fast, composable pair from ProjectDiscovery. **subfinder** does passive subdomain enumeration and nothing else, extremely quickly. **httpx** takes that list and reports which hosts actually answer, with status codes, page titles, technologies and TLS details.

*Why alongside Amass:* different philosophy — Amass is one deep tool, these are Unix pipes. `subfinder -d example.com | httpx -title -tech-detect` gives you a live, annotated inventory in seconds, and slots into a script far more easily. Most practitioners run both and merge.

**Install and run**

```sh
# macOS
brew install subfinder httpx
# Any OS
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
# Run
subfinder -d example.com | httpx -title -tech-detect
```

A Python package also called `httpx` installs a command with the same name. If the wrong one answers, check `where httpx` (Windows) or `which -a httpx` and put Go's bin folder first on your PATH. httpx's README asks for Go 1.25 or newer and warns the project moves fast — read the changelog before updating.

**Links:** [github.com/projectdiscovery/subfinder](https://github.com/projectdiscovery/subfinder) · [github.com/projectdiscovery/httpx](https://github.com/projectdiscovery/httpx)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="wayback"></a>
### Wayback Machine & archive.today
`START` · free · sites

What the site said before they changed it. The Internet Archive's Wayback Machine holds snapshots going back decades; **archive.today** is the complement — it captures on demand, renders JavaScript, and keeps copies of things the Wayback Machine has been asked to remove.

*Two distinct uses.* Historically: old staff pages, old contact details, the un-redacted version of a document. Operationally: **archive anything you find, immediately**, so your evidence survives the page being deleted the day after you cite it. The Wayback CDX API also dumps every URL ever archived under a domain — a free, entirely passive site map.

[web.archive.org](https://web.archive.org/) · [archive.today](https://archive.today/) · CDX: `web.archive.org/cdx/search/cdx?url=*.example.com` · [Common Crawl](https://commoncrawl.org/) for bulk index queries across the whole web

<sub>Last reviewed 2026-11-23</sub>

---

<a id="dns-browser"></a>
### DNSDumpster, Robtex & DNSViz
`START` · free · sites

The no-install layer under [§05](05-domain-ip-network.md)'s command-line tools. **DNSDumpster** maps a domain's hosts, MX, TXT and netblocks and draws the relationships. **Robtex** pivots the other way — given an IP or nameserver, what *else* points at it. **DNSViz** visualizes the DNSSEC chain and shows exactly where validation breaks.

*Why keep browser tools when you have subfinder:* they're instant, they need no setup, and Robtex's reverse pivot in particular — every domain sharing a nameserver or an IP — is a shared-hosting and shared-operator signal the enumeration tools don't hand you directly. Use these first, then reach for the CLI when you need depth or automation.

[dnsdumpster.com](https://dnsdumpster.com/) · [robtex.com](https://www.robtex.com/) · [dnsviz.net](https://dnsviz.net/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="enrichment"></a>
### Indicator enrichment — is this already known bad?
`START` · free tier · sites + APIs

Before you investigate an IP, domain, URL or file hash from scratch, ask whether someone already has. **VirusTotal** for files, URLs and domains across dozens of engines; **AbuseIPDB** for an IP's reported abuse history; **GreyNoise** to tell mass internet background scanning from something aimed at you specifically; **AlienVault OTX** for community pulses; and the **abuse.ch** family — URLhaus, MalwareBazaar, ThreatFox — for malware distribution and current IOCs.

*Why it belongs at the front of this section:* most indicators you'll ever look at are already documented, and five minutes of enrichment saves an hour of original work. **GreyNoise is the one that changes a decision** — "this IP scans the entire internet daily" and "this IP touched only you" are different incidents.

> **Uploading is disclosure.** Submitting a file or URL to VirusTotal can make it public, and submissions are visible to paying subscribers — including, potentially, the adversary who sent it. *Search* by hash rather than uploading whenever you can, and never upload a document from a live investigation or anything containing client data.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="wigle"></a>
### WiGLE — geolocating a Wi-Fi network
`DEEPER` · free account · site + API

A global wardriving database of wireless networks contributed by volunteers, searchable by **BSSID** (the access point's hardware address) or **SSID** (its name). Given either, it returns where that network has been observed — often to street level.

*Why a BSSID is a location:* access points rarely move, so a BSSID in a photo of a router, in a device's saved-network list, or in a leaked config is a physical address. An unusual SSID is nearly as good — a distinctive network name often appears exactly once in the database. The mirror-image lesson is that **your own home SSID is probably in there**, and suffixing it with `_nomap` is what removes it from Google's and Microsoft's equivalents.

[wigle.net](https://wigle.net/) — free account needed to search · [geowifi](https://github.com/GONZOsint/geowifi) queries several such databases at once

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
