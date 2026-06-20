# US-EPG

A custom merged XMLTV feed built from multiple US guide sources and published through GitHub Pages.

## EPG Source URL

Copy the full link below and paste it into the **EPG Source URL** field in your player app:

https://vcicio.github.io/US-EPG/merged_epg.xml.gz

## Source Feeds Used

- `https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS1.xml.gz`
- `https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz`
- `https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz`

## Build Behavior

This project attempts to download all configured source feeds, validate them, merge the valid XMLTV data, trim programmes to the configured date window, and publish the resulting merged guide. The build auto-updates in 6 hour intervals.

If one or more sources fail, the build can still continue as long as at least one source succeeds. When that happens, the generated output and the status section below will indicate that the published EPG may be incomplete.

## Published Site

https://vcicio.github.io/US-EPG/

## Current Source Status
<!-- EPG_STATUS_START -->
Last updated: **2026-06-20 03:00:48 PM CDT**

Programmes kept in latest build: **519569**

Window start: `2026-06-20T19:56:46.505713+00:00`
Window end: `2026-06-30T19:56:46.505713+00:00`

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
