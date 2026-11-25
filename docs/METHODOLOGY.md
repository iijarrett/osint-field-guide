# Methodology

This page explains how the guide is organized, how it relates to the one published standard for this kind of work,
and where it is thin. It is written by hand; the other pages under `docs/` are generated from `data/`.

*Last reviewed 25 November 2026.*

## What this page is, and is not

The guide borrows its vocabulary from the **Berkeley Protocol on Digital Open Source Investigations**, published by
the UN Human Rights Office (OHCHR) and the Human Rights Center at UC Berkeley School of Law in 2020. The Protocol is
written for investigators whose findings may end up in a court or a human-rights process.

This guide is a toolbox, not an implementation of the Protocol. It is not affiliated with or endorsed by either
publisher, and following it does not make an investigation Protocol-compliant. Where this page quotes the Protocol,
it names the chapter so you can read the original: read the Protocol itself before relying on this page's summary.

## The loop and the Protocol's investigative cycle

[Section 00](00-bench-and-loop.md) gives a seven-step loop. The Protocol describes an investigative cycle of six
phases (its Chapter VI: online inquiries, preliminary assessment, collection, preservation, verification and
investigative analysis). They line up like this.

| Guide step | Protocol phase | How they differ |
|---|---|---|
| 1. Scope and authorize | Before the cycle starts | The Protocol's cycle begins at online inquiry. The guide makes scope and authorization an explicit first step because most people who use a guide like this skip it. |
| 2. List your seeds, pick a starting section | Online inquiries | The sections are organized by the identifier you hold, which is the guide's own structure. |
| 3. Collect passive first | Online inquiries, collection | Passive sources first keeps your footprint small and avoids alerting the subject. |
| 4. Capture as you go | Collection, preservation | Capture at the moment of discovery, with URL, UTC time, screenshot and archive link. Pages vanish. |
| 5. Pivot, then re-seed | Back to online inquiries, then preliminary assessment | Each finding is a new selector. The Protocol's preliminary assessment is the question of whether a lead is worth collecting. |
| 6. Verify before it counts | Verification | A finding enters the timeline only after a second, independent source. |
| 7. Analyze and write up | Investigative analysis | A UTC-ordered timeline that keeps what you observed apart from what you inferred. |

The loop is a cycle, not a line: step 5 sends you back to step 2.

## The Protocol's principles, checked against the guide

The Protocol's Chapter II groups its principles as professional, methodological and ethical. The table says honestly
where the guide covers each one and where it does not. "Thin" means the guide touches it but a reader needs more
than the guide gives.

| Principle | Where it shows up in the guide | Coverage |
|---|---|---|
| Accountability | The case folder and log in [section 00](00-bench-and-loop.md); capture discipline in [section 14](14-tradecraft-and-analysis.md) | Covered |
| Competency | Start, deeper and gated tiers; the [skip list](15-skip.md); honest "reviewed on" dates and install-check status | Partly: it says what is hard, it does not train anyone |
| Objectivity | The verification entry ("what would make this false?"); the timeline entry, which keeps observation and inference apart | Covered |
| Legality | The gated tier and the `caution` on each entry; the inclusion bar in [CONTRIBUTING](../CONTRIBUTING.md) | Thin: cautions give the shape of the law, not your jurisdiction's rules |
| Security awareness | Research VM, key vault and leak check in section 00 | Covered |
| Accuracy | Second independent source before a finding counts | Covered |
| Data minimization | Step 1 asks you to write down what you will and will not touch | Thin: the guide does not teach you to limit what you keep |
| Preservation | Archiving tools in section 14 (ArchiveBox, SingleFile, Webrecorder, Hunchly) | Covered |
| Security by design | A separate research machine or profile, one identity per case | Covered |
| Dignity | Gated entries lead with the defensive use; people-search says "the mirror of this is your own exposure" | Partly |
| Humility | Review dates, stated limits, corrections through issues and pull requests | Covered |
| Inclusivity | None | Gap: the tools are mostly English-language and Western-platform-centric |
| Independence | No affiliate links, sponsored placement or tracking links ([the inclusion bar](../CONTRIBUTING.md)) | Covered |
| Transparency | The research-identity entry | Tension, explained below |

## Where the guide and the Protocol pull in different directions

The Protocol's transparency principle is about not misrepresenting yourself online. The research-identity entry in
[section 14](14-tradecraft-and-analysis.md) describes an account that is not the investigator's own, which many
platforms' terms forbid. The guide treats this as a fact of the work, not a recommendation, and puts limits on it:
use it to read, never to interact; never impersonate a real person or organization; check the platform's rules and
your engagement's rules first. If your work falls under the Protocol's standard, or under rules that forbid it,
do not use one.

## Ethics and lawful use

- **Publicly available only.** The guide covers what anyone can see, buy or request. It does not cover getting into
  accounts, systems or private spaces you have no right to, and no entry teaches that.
- **Tools that can hurt people are gated.** Face search, people-search, breach data, dark-web research, mobile-app
  analysis, high-resolution commercial imagery and paid case-capture software carry a tag and a written caution.
  Each caution leads with the lawful, defensive use (looking up your own exposure, auditing your own app) before it
  says what the tool can do to someone else.
- **Aggregation is a harm in itself.** Individually public facts, put together, can identify, locate or expose a
  person. Collect what the question needs, store it with care, and delete what you do not need.
- **Some tools will not be added.** The bar for inclusion rules out anything whose main use is stalking, doxxing,
  credential abuse or access to systems you are not authorized to test.
- **This is not legal advice.** The law differs by country and by use, and changes. The cautions describe the shape
  of the risk; they are not a substitute for a lawyer or for your organization's counsel.

## How entries are chosen and kept

- **The inclusion bar** is in [CONTRIBUTING](../CONTRIBUTING.md): best option for a specific job, maintained or
  honest about its status, dated claims, inspectable installation, ethics in the entry, no affiliate links.
- **Every entry carries a review date** and says how far its install lines were checked. "Partly checked" means
  the Homebrew formula names and PyPI package names were verified; winget IDs and apt package names were not.
- **A weekly health check** ([`scripts/health_check.py`](../scripts/health_check.py)) tests every link and every
  GitHub repository and opens an issue for dead links, moved domains, archived or missing repositories, repositories
  with no push in a year, and entries not reviewed in six months.
- **What the health check cannot tell you:** that a tool still works, that a price or a legal statement is still
  true, or that an entry is the best choice today. A person has to confirm those.

## Limits

- One maintainer. Nobody outside has reviewed the entries for accuracy.
- The guide reflects what was current on its review dates. OSINT tools die faster than most software; check the
  review date and the entry's own status line before you rely on one.
- Many sources block automated requests, so some links are reported as "could not be judged" rather than healthy.
- The install lines have been checked least on Windows and Linux package names, and the health check has not yet
  run against the live network.
- The guide is organized by what you hold. It does not cover every kind of investigation; the Bellingcat toolkit
  below covers target types it leaves out.

## Sources

- *Berkeley Protocol on Digital Open Source Investigations: A Practical Guide on the Effective Use of Digital Open
  Source Information in Investigating Violations of International Criminal, Human Rights and Humanitarian Law*
  (OHCHR and the Human Rights Center, UC Berkeley School of Law, United Nations, 2020, HR/PUB/20/2).
  Publication page: <https://www.ohchr.org/en/publications/policy-and-methodological-publications/berkeley-protocol-digital-open-source>.
  Chapter II sets out the principles (professional, methodological, ethical); Chapter III covers the legal framework,
  including privacy and data protection; Chapter VI covers the investigative process.
- Bellingcat's [Online Investigation Toolkit](https://bellingcat.gitbook.io/toolkit) for target types this guide
  does not cover.
