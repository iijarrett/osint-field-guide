<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a company or organization](06-organization.md) · [Index](../README.md) · [You have a social account or post →](08-social.md)

# 07. You have a photo or video

Imagery is the most satisfying corner of OSINT and the one with the steepest skill curve — most of it is looking carefully, not running something. Two separate questions live here: *where else does this image appear*, and *where and when was it taken*.

| Tool | Tier | Cost and kind |
|---|---|---|
| [ExifTool — read the metadata first](#exif-osint) | `START` | free · local tool |
| [Reverse image search — all four engines](#reverse-image) | `START` | free · sites |
| [Geolocation — the chronolocation toolkit](#geolocation) | `DEEPER` | free · sites · practice |
| [InVID / WeVerify — video verification](#invid) | `DEEPER` | free · browser extension |
| [Facial-recognition search engines](#face-search) | `GATED` | paid · sites |

<a id="exif-osint"></a>
### ExifTool — read the metadata first
`START` · free · local tool

Always the first move. Dumps every embedded field: GPS coordinates, capture timestamp, camera make, model and *serial number*, lens, software used to edit, and often an author or copyright string. On documents it reveals author, organization, and revision history.

*Why first:* it's free, instant, and sometimes ends the investigation on the spot with a GPS tag. When it comes back empty, that's information too — **major platforms strip EXIF on upload**, so a stripped file means it came through a social network, while an intact one means you have an original off a phone or camera. Camera serial numbers link separate photos to one device.

**Install and run**

```sh
# Windows
winget install OliverBetz.ExifTool
# macOS
brew install exiftool
# Linux
sudo apt install libimage-exiftool-perl
# Run
exiftool -a -G1 image.jpg
```

The winget ID was not machine-checked; the Homebrew formula was.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="reverse-image"></a>
### Reverse image search — all four engines
`START` · free · sites

Run the image through **Yandex**, **Google Lens**, **Bing Visual Search** and **TinEye**. They are not interchangeable and the difference is large: Yandex is markedly the strongest at faces, places and visually-similar-but-not-identical images; TinEye is the one that finds *exact* copies and, crucially, sorts by **oldest first** so you can find the original.

*The technique worth knowing:* crop before you search. Feeding the whole photo gets you "generic street scene"; cropping to the one distinctive thing — a shop sign, a bus livery, an unusual building — gets you the location. Run each crop through all four.

[yandex.com/images](https://yandex.com/images/) · [lens.google.com](https://lens.google.com/) · [tineye.com](https://tineye.com/) — and Bing's visual search

<sub>Last reviewed 2026-11-23</sub>

---

<a id="geolocation"></a>
### Geolocation — the chronolocation toolkit
`DEEPER` · free · sites · practice

Pinning an undated, untagged photo to a place and time by reasoning from what's in it. The working set: **Google Earth** and street-level imagery for matching terrain and buildings, **Mapillary** and KartaView for street views where Google has none, **Overpass Turbo** to query OpenStreetMap for features ("every church with a spire within 5km of a river"), and **SunCalc** to derive the time of day and date range from shadow angles.

*Why it's the flagship skill:* this is the technique behind most published open-source investigations, and it's almost entirely analytical — road markings, power pylon design, licence plate format, vegetation, language on signage. The tools just check the hypothesis you formed by looking.

[overpass-turbo.eu](https://overpass-turbo.eu/) · [suncalc.org](https://www.suncalc.org/) · [mapillary.com](https://www.mapillary.com/) · ShadeMap and Shadow Finder for shadow analysis · KartaView · overhead imagery is in [§12](12-tracking.md)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="invid"></a>
### InVID / WeVerify — video verification
`DEEPER` · free · browser extension

The standard verification toolkit for video, built for newsrooms. Splits a video into keyframes so you can reverse-image-search each one, reads platform metadata, magnifies and enhances regions, checks a Twitter/X account's history, and runs forensic filters for manipulation.

*Why it exists as one extension:* video can't be reverse-searched directly — the keyframe step is the whole trick, and doing it by hand is tedious. Increasingly load-bearing now that synthetic video is cheap: the first question about any dramatic clip is whether it's old footage recycled, and keyframe search answers that in a minute.

Extension for Chrome and Firefox — search "InVID WeVerify" in your browser's add-on store

<sub>Last reviewed 2026-11-23</sub>

---

<a id="face-search"></a>
### Facial-recognition search engines
`GATED` · paid · sites

PimEyes and its competitors index faces across the public web and let you search by face rather than by image. Given a photo of a person, they return other photos of the same person from unrelated sites.

*Why it's flagged, not recommended:* it works, it's paid, and it is the single most invasive capability on this guide. It is **restricted or outright unlawful in several jurisdictions** — EU data-protection regulators have taken action against exactly this — and searching a third party's face without a lawful basis is a real legal exposure, not a theoretical one. Know the capability exists, because your adversaries and your clients' harassers use it.

> **The defensive use is the legitimate one.** Searching your *own* face to find out where you appear online is both lawful and genuinely useful, and PimEyes offers an opt-out for exactly that. Anything beyond that needs a documented lawful basis and, in a professional context, written authorization.

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
