<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a ship, an aircraft, or a place seen from above](12-tracking.md) · [Index](../README.md) · [Cross-cutting: tradecraft, capture & analysis →](14-tradecraft-and-analysis.md)

# 13. You suspect a fake — AI-generated or manipulated media

A third of what's worth checking now isn't a person, a domain or a wallet — it's a clip or a photo someone made up. The honest summary of this section is that **provenance tools are strong when they exist, detectors are weak and getting weaker, and context is what holds up**. The picture is moving quickly, so every tool here carries a re-verify-before-you-rely-on flag.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Check provenance first — Content Credentials (C2PA)](#c2pa) | `START` | free · site + CLI |
| [Vendor watermark checkers — SynthID, OpenAI, Meta](#watermark-check) | `START` | free · sites |
| [AI-image detectors — Hive, AI or Not & friends](#ai-detectors) | `DEEPER` | free tier · sites |
| [Image forensics — FotoForensics, Forensically & ExifTool](#image-forensics) | `DEEPER` | free · site + local |
| [Face-swap and voice-clone checks](#deepfake-audio-face) | `DEEPER` | free · sites |
| [The two-indicator rule — context beats classifiers](#two-indicators) | `START` | free · practice |

<a id="c2pa"></a>
### Check provenance first — Content Credentials (C2PA)
`START` · free · site + CLI

C2PA is a signed record, attached to a file by the camera, editor or AI tool that made it, of where it came from and what was done to it. Drop a file into a Content Credentials verifier and it reads and checks that record. **c2patool** is the open-source command-line version.

*Why first:* when a manifest exists and verifies, it answers the question directly. **When it doesn't exist it tells you nothing** — most files carry no credentials, and credentials can be stripped, so a missing manifest means *unknown*, never *clean*.

**Install and run**

```sh
# All OS
cargo install c2patool
#   (needs Rust; or take a release binary from github.com/contentauth/c2pa-rs)
# Run
c2patool <file>
```

[verify.contentauthenticity.org](https://verify.contentauthenticity.org/) — free, browser-based

**Links:** [github.com/contentauth/c2pa-rs](https://github.com/contentauth/c2pa-rs)

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="watermark-check"></a>
### Vendor watermark checkers — SynthID, OpenAI, Meta
`START` · free · sites

The big AI vendors mark what their own tools produce and publish a way to check. Google's **SynthID Detector** reads Google's invisible watermark; OpenAI and Meta each offer a check for their own output. Each recognizes only its own vendor's content.

*Why they're a narrow tool:* a positive is strong evidence, a negative is nearly worthless. Reporting has already shown these checks failing on a photographed screen and on cropped images, and watermark-stripping tools exist. Use them to confirm a suspicion, never to clear a file.

Google SynthID Detector (synthid.com, or ask Gemini) · OpenAI and Meta verification pages — find the current links from each vendor's own site, as the URLs have moved

<sub>Last reviewed 2026-11-23</sub>

---

<a id="ai-detectors"></a>
### AI-image detectors — Hive, AI or Not & friends
`DEEPER` · free tier · sites

Upload an image, get a probability that it's AI-generated. **Hive** is free and among the better-regarded public ones; **AI or Not**, Illuminarty and Sightengine have free tiers or paid APIs.

*Why "one signal":* the accuracy figures vendors quote are their own, and practitioners' consistent finding is that there's still no reliable public detector for the best current AI video. Treat a score as a prompt for human review, and require two or more *independent* indicators before you call something synthetic.

[hivemoderation.com](https://hivemoderation.com/ai-generated-content-detection) · [aiornot.com](https://www.aiornot.com/) — upload only what you have the right to upload (see the VirusTotal note in [§05](05-domain-ip-network.md): uploading is disclosure)

> **A detector score is not a finding.** Never publish "this is AI" on a detector's say-so alone. Record the tool, the date and the score as an observation; the conclusion needs corroboration.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="image-forensics"></a>
### Image forensics — FotoForensics, Forensically & ExifTool
`DEEPER` · free · site + local

Classic manipulation checks that work on any image: **error-level analysis** (FotoForensics, Forensically) highlights regions that were compressed differently from the rest, Forensically also offers clone detection and noise analysis, and **ExifTool** ([§07](07-photo-video.md)) shows the editing software and timestamps.

*Why they still matter:* they test the file rather than guess at the content, so they catch the ordinary Photoshop edit and the recycled screenshot that an AI detector will pass. They are weaker against fully generated images, and error-level analysis can mislead on heavily recompressed files — read it as a hint.

[fotoforensics.com](https://fotoforensics.com/) · [29a.ch/photo-forensics](https://29a.ch/photo-forensics/) — Forensically runs in the browser · ExifTool lines are in [§07](07-photo-video.md)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="deepfake-audio-face"></a>
### Face-swap and voice-clone checks
`DEEPER` · free · sites

**DeepFake-O-Meter** (a university-run service) runs a clip through several open detectors at once and shows where they disagree. **Hiya's Deepfake Voice Detector** is a browser extension for suspect audio. For video, **InVID** ([§07](07-photo-video.md)) breaks a clip into keyframes you can reverse-search.

*Why they sit next to the image tools:* the strongest evidence is usually not the model's verdict but a keyframe that reverse-searches to older footage, or a voice that fails a callback to a known number. Detectors disagree, and that disagreement is itself worth recording.

[DeepFake-O-Meter](https://zinc.cse.buffalo.edu/ubmdfl/deep-o-meter/) · Hiya Deepfake Voice Detector — Chrome extension store

<sub>Last reviewed 2026-11-23</sub>

---

<a id="two-indicators"></a>
### The two-indicator rule — context beats classifiers
`START` · free · practice

Don't call a file synthetic or authentic on one signal. Collect indicators from different domains — provenance, forensics, visual and physical consistency (hands, text, shadows, reflections), and **context**: the earliest upload, the posting account, whether anyone credible was there. Two independent indicators agreeing is a finding; one is a lead. Keep the original file and its hash.

*Why context wins:* the tools above lose ground every time a new generator ships, while "where did this first appear, and who benefits" does not age. Run the reverse-image and earliest-version steps from [§07](07-photo-video.md) and the account checks from [§08](08-social.md) before you reach for a classifier.

Observed (tool, date, score) → inferred (what you conclude) → confidence — keep the three in separate columns of the [§14](14-tradecraft-and-analysis.md) timeline

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
