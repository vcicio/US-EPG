
# US-EPG

A custom merged XMLTV feed built from multiple US guide sources and published through GitHub Pages.

## Full US EPG

The existing full feed is unchanged and includes all configured local, national, and sports guide data. Copy this URL into the **EPG Source URL** field in your player app:

https://vcicio.github.io/US-EPG/merged_epg.xml.gz

## State-Optimized EPGs

These feeds use a 3-day programme window and are intended to load faster. Each includes mapped locals for the state, the shared NFL home-market ABC/CBS/FOX/NBC affiliate bundle, all `US2` channels, and all `US_SPORTS1` channels.

| State | Feed |
|---|---|
| AL | https://vcicio.github.io/US-EPG/states/AL.xml.gz |
| AK | https://vcicio.github.io/US-EPG/states/AK.xml.gz |
| AZ | https://vcicio.github.io/US-EPG/states/AZ.xml.gz |
| AR | https://vcicio.github.io/US-EPG/states/AR.xml.gz |
| CA | https://vcicio.github.io/US-EPG/states/CA.xml.gz |
| CO | https://vcicio.github.io/US-EPG/states/CO.xml.gz |
| CT | https://vcicio.github.io/US-EPG/states/CT.xml.gz |
| DE | https://vcicio.github.io/US-EPG/states/DE.xml.gz |
| FL | https://vcicio.github.io/US-EPG/states/FL.xml.gz |
| GA | https://vcicio.github.io/US-EPG/states/GA.xml.gz |
| HI | https://vcicio.github.io/US-EPG/states/HI.xml.gz |
| ID | https://vcicio.github.io/US-EPG/states/ID.xml.gz |
| IL | https://vcicio.github.io/US-EPG/states/IL.xml.gz |
| IN | https://vcicio.github.io/US-EPG/states/IN.xml.gz |
| IA | https://vcicio.github.io/US-EPG/states/IA.xml.gz |
| KS | https://vcicio.github.io/US-EPG/states/KS.xml.gz |
| KY | https://vcicio.github.io/US-EPG/states/KY.xml.gz |
| LA | https://vcicio.github.io/US-EPG/states/LA.xml.gz |
| ME | https://vcicio.github.io/US-EPG/states/ME.xml.gz |
| MD | https://vcicio.github.io/US-EPG/states/MD.xml.gz |
| MA | https://vcicio.github.io/US-EPG/states/MA.xml.gz |
| MI | https://vcicio.github.io/US-EPG/states/MI.xml.gz |
| MN | https://vcicio.github.io/US-EPG/states/MN.xml.gz |
| MS | https://vcicio.github.io/US-EPG/states/MS.xml.gz |
| MO | https://vcicio.github.io/US-EPG/states/MO.xml.gz |
| MT | https://vcicio.github.io/US-EPG/states/MT.xml.gz |
| NE | https://vcicio.github.io/US-EPG/states/NE.xml.gz |
| NV | https://vcicio.github.io/US-EPG/states/NV.xml.gz |
| NH | https://vcicio.github.io/US-EPG/states/NH.xml.gz |
| NJ | https://vcicio.github.io/US-EPG/states/NJ.xml.gz |
| NM | https://vcicio.github.io/US-EPG/states/NM.xml.gz |
| NY | https://vcicio.github.io/US-EPG/states/NY.xml.gz |
| NC | https://vcicio.github.io/US-EPG/states/NC.xml.gz |
| ND | https://vcicio.github.io/US-EPG/states/ND.xml.gz |
| OH | https://vcicio.github.io/US-EPG/states/OH.xml.gz |
| OK | https://vcicio.github.io/US-EPG/states/OK.xml.gz |
| OR | https://vcicio.github.io/US-EPG/states/OR.xml.gz |
| PA | https://vcicio.github.io/US-EPG/states/PA.xml.gz |
| RI | https://vcicio.github.io/US-EPG/states/RI.xml.gz |
| SC | https://vcicio.github.io/US-EPG/states/SC.xml.gz |
| SD | https://vcicio.github.io/US-EPG/states/SD.xml.gz |
| TN | https://vcicio.github.io/US-EPG/states/TN.xml.gz |
| TX | https://vcicio.github.io/US-EPG/states/TX.xml.gz |
| UT | https://vcicio.github.io/US-EPG/states/UT.xml.gz |
| VT | https://vcicio.github.io/US-EPG/states/VT.xml.gz |
| VA | https://vcicio.github.io/US-EPG/states/VA.xml.gz |
| WA | https://vcicio.github.io/US-EPG/states/WA.xml.gz |
| WV | https://vcicio.github.io/US-EPG/states/WV.xml.gz |
| WI | https://vcicio.github.io/US-EPG/states/WI.xml.gz |
| WY | https://vcicio.github.io/US-EPG/states/WY.xml.gz |
| DC | https://vcicio.github.io/US-EPG/states/DC.xml.gz |

## Source Feeds Used

- `https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS1.xml.gz`
- `https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz`
- `https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz`

## Build Behavior

This project downloads each source once, validates and deduplicates the parsed XMLTV data, publishes the unchanged 10-day full guide, and derives the 3-day state guides from that same in-memory merge. The build auto-updates in 6 hour intervals.

If one or more sources fail, the build can still continue as long as at least one source succeeds. When that happens, the generated output and the status section below will indicate that the published EPG may be incomplete.

## Published Site

https://vcicio.github.io/US-EPG/

## Current Source Status
<!-- EPG_STATUS_START -->
Last updated: **2026-08-21 02:47:31 PM CDT**

Programmes kept in latest build: **393156**

Window start: `2026-08-21T18:55:16.836929+00:00`
Window end: `2026-08-31T18:55:16.836929+00:00`

### Source health

| Source | Status | Notes |
|---|---|---|
| `https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS1.xml.gz` | Working |  |
| `https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz` | Working |  |
| `https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz` | Working |  |

### Summary

- Working sources: **3**
- Failed sources: **0**

All configured sources succeeded in the latest build.

<!-- EPG_STATUS_END -->

## Notes

- The status section above is updated automatically by `scripts/build_epg.py`
- The README is committed automatically by the GitHub Actions workflow
- The generated XML and XML.GZ files are published through GitHub Pages
- `config/station_states.json` contains exact fallback mappings for locals whose channel id lacks state metadata. Unmapped locals are reported in the build log and are not silently assigned to a state.
- `config/nfl_markets.json` defines the shared NFL-market affiliate bundle used in every state feed.
