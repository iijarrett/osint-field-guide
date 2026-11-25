<!-- Generated from data/*.yml by scripts/build_readme.py. Edit the data, not this file. -->

[← You have a wallet address or a token](11-wallets-tokens.md) · [Index](../README.md) · [You suspect a fake — AI-generated or manipulated media →](13-synthetic-media.md)

# 12. You have a ship, an aircraft, or a place seen from above

Aircraft and ships announce themselves on open radio channels, and satellites photograph everything in daylight — so this is the most completely public section after blockchains, and the one where the discipline is knowing what a source can't see. Position data is only as good as its coverage; imagery is only as good as its date and resolution.

| Tool | Tier | Cost and kind |
|---|---|---|
| [Flightradar24, FlightAware & ADS-B Exchange](#air-tracking) | `START` | free tier · sites |
| [MarineTraffic, VesselFinder, Equasis & Global Fishing Watch](#ship-tracking) | `START` | free tier · sites |
| [Free satellite imagery — Copernicus, NASA Worldview & FIRMS, Google Earth Pro](#sat-free) | `START` | free · sites + desktop app |
| [High-resolution and radar imagery](#sat-commercial) | `GATED` | paid · sites |
| [Reading imagery — date, resolution, shadows, clouds](#change-detection) | `DEEPER` | free · practice |

<a id="air-tracking"></a>
### Flightradar24, FlightAware & ADS-B Exchange
`START` · free tier · sites

Live and historical aircraft positions, built from the transponder broadcasts aircraft send in the clear. Flightradar24 and FlightAware have the friendliest interfaces and the deepest history behind a paywall; ADS-B Exchange is the community-fed alternative. **GPSJam** maps where GPS signals are being jammed or spoofed, inferred from aircraft reporting poor navigation accuracy.

*Why it's an investigative source:* an aircraft registration (the tail number) ties to an owner record, and a flight history ties that owner to places and dates. Cross-check the registration against the civil-aviation register for its country. **Know what you're citing:** ADS-B Exchange was acquired by JETNET in 2023, so its "unfiltered" reputation is history (see the Skip list), and military or blocked aircraft are missing or delayed on every one of these.

[flightradar24.com](https://www.flightradar24.com/) · [flightaware.com](https://www.flightaware.com/) · [globe.adsbexchange.com](https://globe.adsbexchange.com/) · [gpsjam.org](https://gpsjam.org/) — no install

> **Public data, private people.** A private jet's movements are public, and a pattern of one person's movements is still a profile of one person. Keep the question about the aircraft or the event, and don't publish a live position for anything that could put someone at risk.

<sub>Last reviewed 2026-11-23</sub>

---

<a id="ship-tracking"></a>
### MarineTraffic, VesselFinder, Equasis & Global Fishing Watch
`START` · free tier · sites

Vessel positions from AIS, the ship-to-ship broadcast system, plus the registry layer behind them. **MarineTraffic** and **VesselFinder** show live and recent tracks. **Equasis** (free account) gives the vessel's IMO number, flag, owner and manager, and inspection history. **Global Fishing Watch** is free and maps fishing activity and gaps in AIS coverage.

*Why the registry layer matters:* a name can change, but the IMO number stays with the hull, so Equasis is how you follow a ship through renamings and reflaggings. **An AIS gap is a lead, not proof** — coverage is patchy and transponders fail — but a ship that goes dark repeatedly near the same place is exactly what sanctions and fisheries investigators look for.

[marinetraffic.com](https://www.marinetraffic.com/) · [vesselfinder.com](https://www.vesselfinder.com/) · [equasis.org](https://www.equasis.org/) · [globalfishingwatch.org](https://globalfishingwatch.org/) — no install; Equasis needs a free account

<sub>Last reviewed 2026-11-23</sub>

---

<a id="sat-free"></a>
### Free satellite imagery — Copernicus, NASA Worldview & FIRMS, Google Earth Pro
`START` · free · sites + desktop app

The free layer of looking at a place from above. The **Copernicus Browser** serves Sentinel imagery (about 10 m per pixel, revisited every few days) with a time slider. **NASA Worldview** is daily, coarse and global, and **NASA FIRMS** maps detected thermal anomalies, i.e. fires. **Google Earth Pro** (free desktop) holds years of historical high-resolution imagery you can scrub through.

*Why they're complementary:* Sentinel and Worldview tell you *when something changed* at the scale of a field, a burn scar or a flooded plain; Earth Pro tells you what it looked like in detail on some earlier date. None of the free sources will show a vehicle, and cloud cover is the usual reason a date you wanted is useless.

**Install and run**

```sh
# Sites: browser.dataspace.copernicus.eu · worldview.earthdata.nasa.gov · firms.modaps.eosdis.nasa.gov
# Windows
winget install Google.EarthPro
# macOS
brew install --cask google-earth-pro
# Linux: download the .deb from google.com/earth/versions
```

Earth Pro's winget ID was not machine-checked; the Homebrew cask was. The imagery sites need no install.

<sub>Last reviewed 2026-11-23 · install lines partly checked (see section 00)</sub>

---

<a id="sat-commercial"></a>
### High-resolution and radar imagery
`GATED` · paid · sites

**Planet** (frequent, mid-resolution), **SkyFi** (order a specific tasking or archive scene by credit card) and **Umbra** (synthetic-aperture radar, which sees through cloud and at night) sell what the free tier can't: detail, frequency and all-weather coverage.

*Why know them:* they're what published investigations of military build-ups and port activity are built on, and a small purchase is sometimes cheaper than the hours of free-imagery guesswork. Pricing and access terms change often — check each site rather than trusting a list.

[planet.com](https://www.planet.com/) · [skyfi.com](https://www.skyfi.com/) · [umbra.space](https://umbra.space/)

<sub>Last reviewed 2026-11-23</sub>

---

<a id="change-detection"></a>
### Reading imagery — date, resolution, shadows, clouds
`DEEPER` · free · practice

Four questions for any overhead image before you claim anything from it: **what date** is this scene really, **what resolution** is it, **where do the shadows fall**, and **what is cloud or haze hiding**. Compare two dates of the same place rather than interpreting one frame, and confirm with a ground-level photo whenever one exists.

*Why it's a step:* most wrong conclusions in this field come from reading a blurry pixel as a thing. Shadow direction and length also date a scene — the sun tools in [§07](07-photo-video.md) (SunCalc, ShadeMap) work on satellite shadows exactly as they do on photo shadows, and the two together locate and date an image.

Pair with [§07](07-photo-video.md) geolocation (Overpass Turbo, Mapillary, SunCalc) and [§14](14-tradecraft-and-analysis.md) capture — save each scene with its date and the viewer's own date label

<sub>Last reviewed 2026-11-23</sub>

---

[← Back to the index](../README.md)
