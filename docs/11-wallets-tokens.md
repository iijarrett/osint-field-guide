<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have source code, a repo, or an app](10-code-and-apps.md) · [Index](../README.md) · [You have a ship, an aircraft, or a place seen from above →](12-tracking.md)

# 11. You have a wallet address or a token

Public blockchains are the most completely open source in this whole guide — every transaction, forever, readable by anyone with no account. That makes tracing genuinely tractable, and it's why this section exists: crypto scams, rug pulls and ransomware payments are ordinary casework now, not a specialism.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Block explorers — read the ledger directly](#block-explorers) | `START` | free · sites |
| [Visual tracing & address clustering](#chain-tracing) | `DEEPER` | free tier · sites |
| [Token & rug-pull checks](#rugpull-checks) | `START` | free · sites |

<a id="block-explorers"></a>
### Block explorers — read the ledger directly
`START` · free · sites

One explorer per chain, all free, no account: **Etherscan** (and the equivalent Arbiscan / BscScan / Polygonscan), **mempool.space** or Blockchain.com for Bitcoin, **Solscan** for Solana, **Tronscan** for Tron. Paste an address and you get every transaction it has ever made, its current balance, its counterparties, and the first time it was funded.

*Why the first funding transaction matters most:* a fresh scam wallet had to get its gas from somewhere, and that source is frequently an **exchange withdrawal** — which means a KYC'd account, which means a real identity sitting behind a subpoena. You can't see who; you can see *which exchange*, and that's the finding. Etherscan's labels also flag known exchange, bridge and mixer addresses for you.

[etherscan.io](https://etherscan.io/) · [mempool.space](https://mempool.space/) · [solscan.io](https://solscan.io/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="chain-tracing"></a>
### Visual tracing & address clustering
`DEEPER` · free tier · sites

Following funds through dozens of hops in a table is unworkable; these draw it as a graph. **Breadcrumbs** and **MetaSleuth** both have usable free tiers for tracing a flow, tagging addresses and saving an investigation. **Arkham** and **Nansen** add entity labels that attribute clusters of addresses to named exchanges, funds and protocols.

*What clustering actually gives you:* one actor usually controls many addresses, and common-input heuristics group them — turning forty addresses into one entity you can reason about. The commercial ceiling is Chainalysis and TRM, which is where law enforcement works; **the free tools get you most of the way for a single scam trace**. Expect the trail to end at a mixer or a cross-chain bridge, and say so plainly when it does rather than guessing past it.

[breadcrumbs.app](https://www.breadcrumbs.app/) · [metasleuth.io](https://metasleuth.io/) · [intel.arkm.com](https://intel.arkm.com/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="rugpull-checks"></a>
### Token & rug-pull checks
`START` · free · sites

Before tracing anything, establish whether the token itself is a trap. The checks that matter: is the contract **verified and its source published**; is liquidity **locked or burned**, or can the deployer withdraw it; does the code contain a **mint, blacklist, or transfer-tax function** the owner can flip; and is the supply concentrated in a handful of wallets. **Token Sniffer**, **GoPlus** and **DEXTools** automate most of this; **rugcheck.xyz** covers Solana.

*Why it's the fast verdict:* an unverified contract holding unlocked liquidity with 90% of supply in the deployer's wallet is a rug pull that hasn't happened yet, and you can establish that in two minutes. Also cross-check the *team* — a "doxxed" founder whose photo reverse-image-searches to a stock library ([§07](07-photo-video.md)) or whose LinkedIn was created last month ([§08](08-social.md)) settles it without touching the chain at all.

[tokensniffer.com](https://tokensniffer.com/) · [GoPlus token security](https://gopluslabs.io/token-security) · [rugcheck.xyz](https://rugcheck.xyz/)

> **None of this is financial advice, and a clean report is not a safe token.** These scanners check contract mechanics, not intent. A technically clean contract can still be run by someone who walks away with the money. This section is for *investigating* a scam, not for deciding what to buy.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
