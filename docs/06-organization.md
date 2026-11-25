<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a domain, IP, or network identifier](05-domain-ip-network.md) · [Index](../README.md) · [You have a photo or video →](07-photo-video.md)

# 06. You have a company or organization

Two halves that feed each other: the *corporate* record — who owns it, who directs it, what it filed — and the *human* layer of who works there and what their email looks like. The second half is the one that leads to a phishing simulation or a social-engineering assessment, which is why it's also the half to understand defensively.

| Tool | Tier | Cost and kind |
|---|---|---|
| [OpenCorporates & national registries](#opencorporates) | `START` | free tier · sites |
| [SEC EDGAR & OCCRP Aleph](#edgar-aleph) | `DEEPER` | free · sites |
| [OpenSanctions, ICIJ Offshore Leaks & Open Ownership](#sanctions-ownership) | `START` | free · sites |
| [theHarvester](#theharvester) | `DEEPER` | free · local tool · Python |
| [Tech-stack fingerprinting & job postings](#tech-stack) | `DEEPER` | free tier · sites + extension |
| [Shared tracker & analytics IDs](#tracker-ids) | `DEEPER` | free · sites + view-source |

<a id="opencorporates"></a>
### OpenCorporates & national registries
`START` · free tier · sites

OpenCorporates aggregates company registries worldwide into one searchable database — legal name, jurisdiction, incorporation date, officers, and filings. Behind it sit the national sources: Companies House (UK), the state Secretary of State registries (US), and their equivalents elsewhere.

*Why start here:* officers and directors are **named humans with addresses**, which is the pivot from an organization straight back to section 04. Shell-company structures become visible when the same three names appear as directors across nine entities.

[opencorporates.com](https://opencorporates.com/) — go to the national registry directly for the authoritative filing

<sub>Last reviewed 2026-11-23</sub>

---

<a id="edgar-aleph"></a>
### SEC EDGAR & OCCRP Aleph
`DEEPER` · free · sites

**EDGAR** holds every filing by a US public company — annual reports, executive compensation, ownership stakes, subsidiary lists, and the named signatories. **Aleph** is OCCRP's investigative archive: leaked datasets, sanctions and watch lists, court records and corporate registries from across the world, all cross-searchable.

*Why these two:* EDGAR's Exhibit 21 subsidiary list maps a corporate group in one document, and its filings name real executives with real signatures. Aleph is the single best place to check a name or entity against leaks, sanctions and offshore records at once — built by journalists, free, and genuinely deep.

[sec.gov/edgar/search](https://www.sec.gov/edgar/search/) · [aleph.occrp.org](https://aleph.occrp.org/) — moved onto OCCRP's new Aleph Pro infrastructure in Dec 2025; **the public instance stays free**

<sub>Last reviewed 2026-11-23</sub>

---

<a id="sanctions-ownership"></a>
### OpenSanctions, ICIJ Offshore Leaks & Open Ownership
`START` · free · sites

The beneficial-ownership and watch-list layer. **OpenSanctions** consolidates sanctions lists and politically-exposed-person data into one searchable, matchable database. The **ICIJ Offshore Leaks Database** makes the Panama, Paradise and Pandora Papers searchable. **Open Ownership** publishes beneficial-ownership registers where countries release them.

*Why after OpenCorporates:* a company record names a director; these tell you whether the director, or the real owner behind a shell, is sanctioned, politically exposed or sitting in a leak. Run a name here before you build a picture of a company's people. A match is a *lead* — names collide, so confirm with a date of birth or a second record.

[opensanctions.org](https://www.opensanctions.org/) · [offshoreleaks.icij.org](https://offshoreleaks.icij.org/) · [openownership.org](https://www.openownership.org/) — check OpenSanctions' licence: free for non-commercial use, a licence for business use

<sub>Last reviewed 2026-11-23</sub>

---

<a id="theharvester"></a>
### theHarvester
`DEEPER` · free · local tool · Python

The classic organizational recon tool: give it a domain and it sweeps search engines, certificate logs, PGP key servers and data sources for **email addresses, employee names, subdomains and hosts** associated with it. One command, broad sources.

*Why it's still standard:* it's the fastest way to assemble the human attack surface of an organization, and it's preinstalled on Kali. Combine its output with the email pattern from Hunter.io in section 02 and you have the full construct-any-address capability.

**Install and run**

```sh
# All OS
git clone https://github.com/laramies/theHarvester ; cd theHarvester ; uv sync
# Run
uv run theHarvester -d example.com -b crtsh,certspotter
# Kali: preinstalled
```

As of its README on 23 Nov 2026 the current release is 4.11.1 and asks for a very recent Python; `uv` fetches the right one for you. On Windows run it inside WSL. Source at github.com/laramies/theHarvester.

**Links:** [github.com/laramies/theHarvester](https://github.com/laramies/theHarvester)

> **Don't install it from PyPI.** The `theHarvester` package on PyPI is an abandoned placeholder — version 0.0.1 from 2019, nothing to do with the real project. `pip install theHarvester` gets you a stub. Use Kali's copy or install from the GitHub repo.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="tech-stack"></a>
### Tech-stack fingerprinting & job postings
`DEEPER` · free tier · sites + extension

What an organization *runs*, established two ways. **Wappalyzer** or **BuiltWith** fingerprint a site's stack from the browser. And their **job postings** list it outright — "experience with Okta, CrowdStrike, ServiceNow and Azure AD required" is a free internal architecture diagram.

*Why job ads are the sleeper source:* no tool needed, entirely passive, and organizations publish their security stack, their cloud provider and their internal tooling voluntarily because they have to hire. The defensive lesson is identical — **read your own postings and see what you're advertising**.

[wappalyzer.com](https://www.wappalyzer.com/) — browser extension, free tier; then just read the careers page

<sub>Last reviewed 2026-11-23</sub>

---

<a id="tracker-ids"></a>
### Shared tracker & analytics IDs
`DEEPER` · free · sites + view-source

The highest-yield infrastructure pivot on this guide. A site's page source carries identifiers its operator reused across everything they run — a Google Analytics `UA-`/`G-` tag, an AdSense publisher ID, a Facebook Pixel, a Matomo site ID. Search those strings and you get every other site the same person set up.

*Why it beats WHOIS now:* registration privacy hides the owner, but analytics IDs are pasted into the page by hand and almost nobody thinks to vary them. This is the single technique that most reliably links a network of scam sites, a shell-company web presence, or a disinformation cluster to one operator. Also pivot on **favicon hashes** and unique script paths via urlscan's search.

Read the page source, or use [analyzeid.com](https://analyzeid.com/) / [spyonweb.com](https://spyonweb.com/) · then confirm the set with a urlscan.io search on the same ID

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
