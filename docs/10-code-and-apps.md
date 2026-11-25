<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You want breach & credential exposure](09-breach-credentials.md) · [Index](../README.md) · [You have a wallet address or a token →](11-wallets-tokens.md)

# 10. You have source code, a repo, or an app

The section most OSINT guides leave out, and the one that most reliably finds something an organization did not mean to publish. Developers commit credentials, internal hostnames, S3 buckets and API keys constantly, and the search engines over public code are excellent. Same technique, two intents: an attacker hunting a way in, and a defender auditing what their own team has leaked.

| Tool | Tier | Cost and kind |
|---|---|---|
| [GitHub code search & dorking](#github-dorking) | `START` | free account · site |
| [grep.app, Sourcegraph, GitLab & Searchcode](#code-search-engines) | `DEEPER` | free tier · sites |
| [TruffleHog](#secret-scanners) | `DEEPER` | free · local tools |
| [Pulling intelligence out of a mobile app](#apk-analysis) | `GATED` | free · local tools |

<a id="github-dorking"></a>
### GitHub code search & dorking
`START` · free account · site

GitHub's code search reads the contents of public repositories, and its qualifiers make it a targeted instrument: `org:`, `user:`, `language:`, `path:`, `filename:`. Combine an organization's name or domain with the shape of a secret — `"example.com" AND (password OR api_key OR BEGIN RSA)`, or `filename:.env`, `filename:config.json`, `path:.aws credentials`.

*Why it's the first stop:* a single committed `.env` file can contain a live database password, and people commit them weekly. Beyond credentials it maps an organization's internal naming — hostnames, service names, staff usernames in commit metadata, which cloud provider they use. **Commit history is the sharp edge**: a secret deleted in a later commit is still in the history and still searchable.

Signed-in search at [github.com/search](https://github.com/search) — needs an account for code search

> **Finding a credential is where you stop.** A live key in a public repo is a *finding*, to be reported to its owner. Using it is unauthorized access and a criminal offence — the fact that it was published by accident changes nothing. Report through a security.txt contact, a bug-bounty program, or the repo owner directly.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="code-search-engines"></a>
### grep.app, Sourcegraph, GitLab & Searchcode
`DEEPER` · free tier · sites

GitHub is not the only forge, and its own search has quirks. **grep.app** does fast literal and regex search across a large slice of public GitHub with no login at all — the quickest way to test whether a distinctive string exists anywhere. **Sourcegraph** searches across multiple hosts with real structural queries. **GitLab** and **Searchcode** reach repos GitHub-only searching never sees.

*Why run more than one:* each indexes a different corpus, and a secret pushed to a self-hosted GitLab mirror or an obscure forge is exactly the one nobody has found yet. grep.app's regex support is also better for hunting a pattern — an internal hostname format, a key prefix — rather than a known string.

[grep.app](https://grep.app/) · [sourcegraph.com](https://sourcegraph.com/search) · [gitlab.com/search](https://gitlab.com/search) · [searchcode.com](https://searchcode.com/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="secret-scanners"></a>
### TruffleHog
`DEEPER` · free · local tools

Automate the above against a repo you can clone. **TruffleHog** walks the **entire commit history** looking for credential patterns — hundreds of detectors for specific providers — and then *verifies* many of the keys it finds by testing whether they still authenticate, which separates a dead 2019 token from a live one.

*Why verification is the whole value (TruffleHog v3.99 as of November 2026):* raw regex scanning produces overwhelming false positives, and a report full of expired keys gets ignored. "Seventeen matches, three still valid" is actionable. Point these at your own organization's repos on a schedule — this is the defensive use, and it's the one you'll run most.

**Install and run**

```sh
# macOS
brew install trufflehog
# Docker
docker run --rm -it trufflesecurity/trufflehog:latest github --repo https://github.com/<org>/<repo>
# Win/Linux: download the release for your OS from github.com/trufflesecurity/trufflehog/releases
# Run local
trufflehog git file://. --only-verified
```

Upstream's README also shows a curl-to-shell installer; this guide prefers brew, Docker or the release binary so you can inspect what you run.

**Links:** [github.com/<org](https://github.com/<org) · [github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="apk-analysis"></a>
### Pulling intelligence out of a mobile app
`GATED` · free · local tools

An APK is a zip file full of evidence. Static analysis surfaces the **backend endpoints** the app talks to (frequently including staging and internal APIs), **hardcoded keys and tokens**, the **third-party SDKs and trackers** embedded in it, the permissions it requests, and signing-certificate details that link separate apps to one developer.

*Why it's an OSINT source and not just an appsec task:* the endpoint list is an attack-surface map the organization never published, and the SDK inventory tells you who they share data with. **MobSF** is the standard one-stop analyzer; **apktool** and **jadx** do the decompilation by hand; **Exodus Privacy** gives you the tracker list with no install at all. Gated here because it needs a sandbox, real time, and clear authorization.

**Install and run**

```sh
# Docker
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
#   (then open http://localhost:8000)
# macOS
brew install jadx
# Linux
sudo apt install jadx
#   (Kali) — or the release zip
# Windows: download the jadx release zip from github.com/skylot/jadx/releases
```

[MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) in Docker · [jadx](https://github.com/skylot/jadx) for readable decompiled source · [Exodus Privacy](https://reports.exodus-privacy.eu.org/) for the tracker report with no install at all.

> **Analyze in a VM, and check the licence.** Run an unknown APK's analysis in a disposable VM, never install it on a real device, and remember that reverse-engineering a third party's app may breach its terms of service or local law even when the file is public.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

[← Back to the index](../README.md)
