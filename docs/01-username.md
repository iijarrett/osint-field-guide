<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← Before you start: the bench and the loop](00-bench-and-loop.md) · [Index](../README.md) · [You have an email address →](02-email.md)

# 01. You have a username

The single most productive starting selector there is. People reuse handles across a decade of accounts without ever thinking about it — the gaming forum from 2013 and the professional profile from last month share a name, and that link is usually the whole investigation. Run all three of these; they use different site lists and disagree constantly.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Maigret](#maigret) | `START` | free · local tool · Python |
| [Sherlock](#sherlock) | `START` | free · local tool · Python |
| [Blackbird](#blackbird) | `START` | free · local tool · Python |
| [WhatsMyName](#whatsmyname) | `START` | free · site + dataset |
| [Manual handle pivoting](#handle-pivot) | `DEEPER` | free · practice |

<a id="maigret"></a>
### Maigret
`START` · free · local tool · Python

Checks a username against thousands of sites and — the part that matters — **parses what it finds**, pulling names, bios, avatars, linked accounts and IDs off each hit into a single dossier. Exports to HTML, PDF and JSON. A fork of Sherlock that grew well past it.

*Why first:* the extraction step saves you opening 40 tabs by hand, and it's the most actively developed of the three — version 0.6.7 is current on PyPI as of November 2026. Where Sherlock says "account exists," Maigret says "account exists, and here's the display name and the linked Twitter."

**Install and run**

```sh
# All OS
pipx install maigret
# Run
maigret <username> --html
```

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="sherlock"></a>
### Sherlock
`START` · free · local tool · Python

The original and still the best-known username hunter — checks one handle across 400+ social networks and reports where it exists. Fast, simple output, no parsing. Ships preinstalled in Kali.

*Why still run it:* different site list from Maigret, and actively maintained (0.16.2, September 2026). Running both and comparing is standard practice — each catches sites the other misses. Treat every hit as a *lead*, not a fact: common handles collide, and plenty of sites return a false positive on any string you give them.

**Install and run**

```sh
# All OS
pipx install sherlock-project
# Run
sherlock <username>
# Kali: already installed
```

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="blackbird"></a>
### Blackbird
`START` · free · local tool · Python

A username and email search tool in the same family as Maigret and Sherlock. It checks a handle against 600-plus sites using the WhatsMyName dataset, can export results to PDF and CSV, and has an optional AI-profiling feature that summarizes what it found.

*Why a second pick:* a different front end over the community dataset, and actively developed — its repository shows hundreds of commits and many stars. The AI summary sends your findings to a third-party service; leave it off for anything sensitive. Treat every hit as a lead, as with the other two.

**Install and run**

```sh
# All OS
git clone https://github.com/p1ngul1n0/blackbird ; cd blackbird
# Windows
python -m venv .venv ; .venv\Scripts\activate ; pip install -r requirements.txt
# macOS/Linux
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
# Run
python blackbird.py --username <handle>
```

Install steps follow the project's README layout; read `requirements.txt` before installing and keep it in the research VM. There is a PyPI package named `blackbird`, but it was not confirmed to be this project, so this guide doesn't use it.

**Links:** [github.com/p1ngul1n0/blackbird](https://github.com/p1ngul1n0/blackbird)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="whatsmyname"></a>
### WhatsMyName
`START` · free · site + dataset

A community-maintained JSON dataset of 700+ sites and their account-detection rules, plus a web front end you can just type into. No install needed for the basic use.

*Why it matters:* it's the **data layer half the other tools are built on**, and it's curated harder than any single scanner's built-in list — detection rules get fixed when a site changes. Use the web version for a quick check; pull the JSON when you're building something.

[whatsmyname.app](https://whatsmyname.app/) · dataset at [github.com/WebBreacher/WhatsMyName](https://github.com/WebBreacher/WhatsMyName)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="handle-pivot"></a>
### Manual handle pivoting
`DEEPER` · free · practice

The scanners only check the handle you gave them. People mutate: `jsmith` becomes `j_smith`, `jsmith88`, `smithj`, `jsmithdev`. Build the variant list by hand and re-run. Then search the raw handle as a quoted string in a normal search engine — forum posts, commit logs and pasted profiles surface things no enumerator touches.

*Why it's listed as a step:* this is where most of the actual findings come from, and no tool does it for you. The number on the end is usually a birth year. The prefix is usually a real name. Both are pivots into section 04.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
