<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a username](01-username.md) · [Index](../README.md) · [You have a phone number →](03-phone.md)

# 02. You have an email address

An email address is the master key of the modern internet — it's the login for nearly everything, so establishing which services it's registered at maps a person's whole digital footprint. Most of the technique exploits the same design flaw: password-reset and sign-up flows leak whether an address is known.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Epieos](#epieos) | `START` | free tier · site |
| [GHunt](#ghunt) | `DEEPER` | free · local tool · Python |
| [holehe](#holehe) | `DEEPER` | free · local tool · stale |
| [Hunter.io & email-format guessing](#hunterio) | `DEEPER` | free tier · site |
| [Reading the headers, not just the address](#email-headers) | `START` | free · practice + sites |

<a id="epieos"></a>
### Epieos
`START` · free tier · site

Paste an email or phone number and get back the services it's registered with, plus any linked Google account data — profile name, photo, public reviews, calendar if it's exposed. The fastest single lookup in this section.

*Why first:* zero setup, and the Google half alone often resolves an anonymous address to a real name and face. The free tier is genuinely useful; paid unlocks depth. Run it before you install anything.

[epieos.com](https://epieos.com/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="ghunt"></a>
### GHunt
`DEEPER` · free · local tool · Python

A Google-account investigation framework. Feed it a Gmail address or a Google account ID and it extracts the profile name and photo, the account's public Maps reviews and photos, YouTube channel, Play Store reviews, and Calendar if the user left it public.

*Why it's worth the setup:* a Gmail address is extraordinarily common as a person's primary identity, and this is the deepest free extraction of it. Maps reviews in particular are a goldmine — people review their own gym, their local coffee shop, their dentist, quietly mapping where they live.

**Install and run**

```sh
# All OS
pipx install ghunt
# Then
ghunt login
#   (paste cookies from a throwaway Google account, never your own)
```

> **Use a burner Google account.** GHunt authenticates as a real Google session.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="holehe"></a>
### holehe
`DEEPER` · free · local tool · stale

Checks an email address against 120-odd sites by abusing their password-recovery and registration flows — no email is ever sent to the target, it just reads what the form reveals. Tells you where an address is registered.

*Why the caveat:* the technique is sound and it still finds things, but **the last release was 1.61 in July 2022**. Four years of sites changing their reset flows means a lot of silent false negatives now. Run it, believe the hits, don't trust the misses — and cross-check against Epieos above. A newer tool in the same space, **user-scanner** (`pipx install user-scanner`), says it is actively maintained and is on PyPI, but it is young and its author promotes it, so verify its hits the same way.

**Install and run**

```sh
# All OS
pipx install holehe
# Run
holehe <email>
```

Accurate where it works, quietly out of date where it doesn't — PyPI still lists 1.61 as the latest release.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="hunterio"></a>
### Hunter.io & email-format guessing
`DEEPER` · free tier · site

The reverse direction: given a *domain*, what do that organization's email addresses look like, and which ones are known? Hunter reports the pattern — `first.last@`, `flast@`, `first@` — and lists addresses it has seen, with a confidence score.

*Why it matters:* once you know the pattern and have a staff list from section 06, you can construct an entire organization's email addresses from names alone. This is the exact pivot phishing operators use, which is why knowing it is defensive work too. Free tier is capped at a small number of searches a month.

[hunter.io](https://hunter.io/) — free tier needs an account; verify guesses before relying on them

<sub>Last reviewed 2026-11-23</sub>

---

<a id="email-headers"></a>
### Reading the headers, not just the address
`START` · free · practice + sites

A different question from the rest of this section: not "where is this address registered" but "where did this *message* actually come from." The full headers record every server the mail passed through. Read `Received:` bottom-up — the earliest hop is closest to the sender — then check `Return-Path` against the display name, and whether **SPF, DKIM and DMARC** passed.

*Why it's the fastest phishing verdict there is:* a message claiming to be from a bank whose first hop is a residential IP in an unrelated country, with SPF failing, is settled in thirty seconds. The originating IP then drops straight into [§05](05-domain-ip-network.md). Get the raw headers from "Show original" (Gmail) or "View source" / message properties (Outlook) — the summary view hides exactly the fields you need.

Paste into [mha.azurewebsites.net](https://mha.azurewebsites.net/) (Microsoft's Message Header Analyzer) or Google's [Messageheader](https://toolbox.googleapps.com/apps/messageheader/) — both parse the hops into a readable table

> **Headers below the first trusted hop are forgeable.** Anything a sender controls can be faked, so `Received` lines can be fabricated from the bottom up. Trust the hops added by *your own* mail infrastructure, and treat the rest as claims. SPF/DKIM/DMARC results are the part that can't be spoofed.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
