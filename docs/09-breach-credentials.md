<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a social account or post](08-social.md) · [Index](../README.md) · [You have source code, a repo, or an app →](10-code-and-apps.md)

# 09. You want breach & credential exposure

The section that runs in both directions most obviously. Checking an organization's exposed credentials is standard pre-engagement work and standard defensive monitoring; the difference is entirely authorization. It's also the section with the sharpest legal edge — see the caution below.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Have I Been Pwned](#hibp) | `START` | free · site + paid API |
| [Commercial breach-data search](#breach-search) | `GATED` | paid · sites |
| [Run this whole guide on yourself](#self-exposure) | `START` | free · practice |

<a id="hibp"></a>
### Have I Been Pwned
`START` · free · site + paid API

The reputable, ethical breach index. Tells you which breaches an address appears in and what data classes each exposed — but never shows you a password. **Domain search** lets a verified domain owner see every breached address across their whole organization, which is the defensive killer feature.

*Why it's the one to start with:* run by Troy Hunt, transparent about sources, and deliberately designed not to be an attack tool. For your own exposure and your own domain it's free and authoritative. The API is paid but cheap, and the k-anonymity password endpoint lets you check passwords without ever sending one.

**Links:** [haveibeenpwned.com](https://haveibeenpwned.com/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="breach-search"></a>
### Commercial breach-data search
`GATED` · paid · sites

DeHashed, Intelligence X, Snusbase and similar go further than HIBP: they index the breach *contents* and let you search by email, username, name, phone, IP or hashed password, returning the actual records. Intelligence X additionally archives darknet, document and leak material with its own historical snapshots.

*Why these are gated here:* they are powerful, they are used legitimately by CTI teams and incident responders every day, and they are also one subpoena away from being the worst thing in your browser history if you can't explain why you ran a query. Subscription-based, and you should be able to justify every lookup.

> **Searching is not the same as using.** Querying breach data about your own organization under authorization is normal professional work. Using a credential you found to *log into* anything is unauthorized access — a serious criminal offence in essentially every jurisdiction, regardless of how the password reached you. The line is bright and it is not about where the data came from.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="self-exposure"></a>
### Run this whole guide on yourself
`START` · free · practice

Take your own name, your own handles, your own email and work sections 01 through 08 against yourself (and 10 if you write code). Write down everything you find and where it came from.

*Why it's the best exercise on the page:* you have ground truth. You know which hits are wrong, which aggregator merged you with a stranger, and which forgotten 2014 account is still sitting there with your real name on it — so you learn what these sources actually do, not what they claim.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
