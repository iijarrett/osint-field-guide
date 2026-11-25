<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a photo or video](07-photo-video.md) · [Index](../README.md) · [You want breach & credential exposure →](09-breach-credentials.md)

# 08. You have a social account or post

The hardest-hit area of OSINT in recent years. The API shutdowns of 2023 killed most of the automated social tooling that guides still recommend, and what replaced it is manual work plus archives. Be suspicious of any social OSINT tutorial that hasn't been updated recently — much of it now describes tools that simply don't function.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Native platform search, used hard](#platform-search) | `START` | free · practice |
| [Mastodon, the Fediverse & Bluesky](#fediverse-bluesky) | `DEEPER` | free · sites + practice |
| [Deleted posts & social archives](#social-archives) | `START` | free · sites |
| [Telegram & Discord](#telegram-discord) | `DEEPER` | free · sites + accounts |
| [Telling a real account from a fake one](#bot-detection) | `DEEPER` | free · practice |
| [Dark-web research, safely](#darkweb) | `GATED` | free · Tor + sites |

<a id="platform-search"></a>
### Native platform search, used hard
`START` · free · practice

Each platform's own advanced search, which almost nobody uses to capacity. X/Twitter's advanced search filters by account, date range, replies-to and geocode. Reddit supports `author:` and `subreddit:`. LinkedIn filters by company, title and location. Facebook's search is weak but its *public* friend lists and photo tags are not.

*Why this leads now:* with the APIs closed, the native interface is frequently the **only** thing that still works. A date-bounded advanced search on one account beats any scraper that 403s. Pair with `site:` operators from section 04 to reach what the platform's own search hides.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="fediverse-bluesky"></a>
### Mastodon, the Fediverse & Bluesky
`DEEPER` · free · sites + practice

The decentralized social networks work differently from the closed ones. **Mastodon** posts live on whichever server the account joined, and full-text search of posts is opt-in per account, so search is deliberately weak — work through hashtag timelines, the home server's public profile, and `site:` operators. **Bluesky** profiles and posts are public by default and readable without an account, and a handle can be verified through DNS, which makes the domain behind a custom handle a pivot back to [§05](05-domain-ip-network.md).

*Why a separate entry:* the tools built for the closed platforms mostly don't reach here, and almost no OSINT guide covers it. Bellingcat's toolkit lists **BskyFollowFinder** for mapping who follows whom on Bluesky and **Hoaxy** for tracing how a link or claim spreads across Bluesky and X.

Bluesky: [bsky.app](https://bsky.app/) (no login to read) · Mastodon: the home server's `/@username` page · both: archive first — [web.archive.org](https://web.archive.org/), [archive.today](https://archive.today/)

> **Federation copies things.** A post deleted on one server can survive on others that already pulled it. Capture before you contact or react, and remember that an account's home server is its jurisdiction — a report to a trust-and-safety team goes to that server's admins.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="social-archives"></a>
### Deleted posts & social archives
`START` · free · sites

People delete. Archives remember. The Wayback Machine holds snapshots of public profiles; archive.today captures dynamic pages the Wayback Machine struggles with; Google and Bing caches occasionally hold a recently-removed page; and third-party mirrors preserve deleted content on several platforms.

*Why it's the highest-yield social technique:* the post someone deleted is almost always the interesting one, and the act of deletion is itself a finding. **Archive first, read second** — the moment a subject notices attention, things start disappearing.

Same tools as [§05](05-domain-ip-network.md) — [web.archive.org](https://web.archive.org/) and [archive.today](https://archive.today/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="telegram-discord"></a>
### Telegram & Discord
`DEEPER` · free · sites + accounts

Where a great deal of threat-actor and extremist activity actually lives. Telegram's public channels are indexed by several third-party search sites and are genuinely open; Discord requires joining a server but leaks user IDs, join dates and cross-server presence once you're in.

*Why it's essential for threat intel:* ransomware leak sites, initial-access brokers, credential markets and hacktivist coordination run on these platforms now, and monitoring them is mainstream CTI work. **Telegram usernames pivot straight back to section 01**, and the same handle is often reused across markets and forums.

Telegram search engines and trackers listed by Bellingcat: Telegago, TGStat, Telemetrio, TelegramDB — all browser-based, no install · Telepathy is listed there as unmaintained, so it is on the Skip list

> **Joining is participation.** Entering a server or channel is active, logged, and visible to admins. Use a burner identity on a separate machine, never interact, and be clear on your authorization — passively reading a public channel and engaging with a criminal marketplace are very different acts, legally and ethically.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="bot-detection"></a>
### Telling a real account from a fake one
`DEEPER` · free · practice

Judged on behaviour, not vibes. The signals that actually discriminate: **creation date versus activity volume** (an account made last month with 8,000 posts), **posting rhythm** (activity at a constant rate around the clock, or confined to one timezone's working hours regardless of claimed location), **a profile photo that reverse-image-searches** to a stock library or another person, **follower-to-following ratio and follower quality**, and near-identical phrasing appearing across accounts within minutes.

*Why no tool is listed:* the automated "bot score" services are unreliable and several well-known ones have shut down or gone paid with no transparency about their model. The manual signals above are more defensible and you can show your work. **Coordination is the stronger finding anyway** — one suspicious account proves little; fifty accounts posting the same sentence within a two-minute window is a network, and that's what you report.

> **"Bot" is a conclusion, not an observation.** Record what you saw — creation date, posting frequency, reused photo — and let the label follow. Plenty of real people post constantly, use a stock avatar, or have few followers; calling a real person's account fake in a published finding is the kind of error that ends credibility.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="darkweb"></a>
### Dark-web research, safely
`GATED` · free · Tor + sites

Where leaked data, ransomware victim postings and criminal marketplaces are published. **Ahmia** indexes onion sites and is reachable from the clear web; **ransomware leak-site trackers** (ransomwatch and similar) aggregate victim postings so you don't have to visit the sites at all; several CTI vendors publish free dark-web search front ends.

*Why the clear-web mirrors come first:* for most questions — "has my organization been named on a leak site," "is this breach real" — a tracker answers it without ever opening Tor. Go direct only when the tracker doesn't cover it, and then through **Tor Browser in a disposable VM**, never your daily machine.

[ahmia.fi](https://ahmia.fi/) — clear-web onion index, filters known-abusive content

> **Reading is not the risk; interacting is.** Downloading leaked data, registering on a marketplace, or contacting a seller moves you from observation to participation and can be a criminal offence regardless of intent. Never download a breach dump "to verify it," never create an account on a criminal forum without explicit written authorization, and know that some content is illegal to possess the instant it renders.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
