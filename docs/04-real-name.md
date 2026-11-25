<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a phone number](03-phone.md) · [Index](../README.md) · [You have a domain, IP, or network identifier →](05-domain-ip-network.md)

# 04. You have a real name

The hardest selector to work, because names are not unique and the good sources are jurisdictional. This is where OSINT stops being tool-driven and becomes records research — and where the ethical weight gets heaviest, because everything here is about a specific identifiable human being.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Search operators, used properly](#search-operators) | `START` | free · practice |
| [People-search aggregators](#people-search) | `GATED` | free & paid · sites |
| [Court, property & voter records](#public-records) | `DEEPER` | free & paid · sites |
| [Obituaries & genealogy sources](#genealogy) | `DEEPER` | free tier · sites |

<a id="search-operators"></a>
### Search operators, used properly
`START` · free · practice

The unglamorous skill that outperforms most tools. `"exact phrase"` for names, `site:` to pin a platform, `filetype:pdf` for documents, `intitle:` and `inurl:` for structure, `-term` to cut noise. Combine them: `"Jane Smith" site:linkedin.com`, or `"Jane Smith" filetype:pdf` to find her in a conference programme or a board minutes PDF.

*Why it leads this section:* a specialized tool searches a fixed list of sites. An operator query searches the indexed web. For a name, the second one wins more often than people expect — and **run the same query on Bing and DuckDuckGo too**, since their indexes and their tolerance for operator queries differ from Google's.

The Google Hacking Database at [exploit-db.com/google-hacking-database](https://www.exploit-db.com/google-hacking-database) catalogs the heavy-duty patterns

<sub>Last reviewed 2026-11-23</sub>

---

<a id="people-search"></a>
### People-search aggregators
`GATED` · free & paid · sites

The data-broker layer — Spokeo, BeenVerified, TruePeopleSearch, Whitepages, FastPeopleSearch and dozens more. They aggregate public records, marketing databases and scraped social data into a profile: addresses, relatives, phone numbers, age.

*Why to treat carefully:* the data is often **wrong, stale, or about a different person with the same name** — aggregators merge records aggressively and never correct. Use them to generate leads you then confirm in a primary source, never as a finding on their own. The free tiers are mostly a teaser for a subscription.

> **The mirror of this is your own exposure.** These sites hold a profile on you right now.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="public-records"></a>
### Court, property & voter records
`DEEPER` · free & paid · sites

The primary sources the aggregators are scraping. In the US: **CourtListener / RECAP** for federal case documents (free, and a genuine public good), **PACER** for the official federal docket (paid per page), county assessor and recorder sites for property ownership, and state business registries. Many jurisdictions publish voter rolls.

*Why it beats the aggregators:* it's authoritative, dated, and citable. A property record naming an owner at an address is evidence; a Spokeo profile saying the same thing is a rumor. Slower, jurisdiction-specific, and worth the time when the finding has to hold up.

[courtlistener.com](https://www.courtlistener.com/) — free federal case law and dockets via the RECAP archive

<sub>Last reviewed 2026-11-23</sub>

---

<a id="genealogy"></a>
### Obituaries & genealogy sources
`DEEPER` · free tier · sites

Obituaries name the entire family — spouse, children, siblings, the town they live in, sometimes employers — in one indexed, permanent document. FamilySearch, FindAGrave and newspaper archives make them searchable.

*Why investigators love them:* a single obituary can resolve a family network that would take days to assemble any other way, and people who scrub their own online presence rarely think about a relative's death notice from 2011. It's also a reminder that **your exposure includes what other people publish about you**.

[familysearch.org](https://www.familysearch.org/) — free with an account

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
