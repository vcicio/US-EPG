# US-EPG

A custom merged XMLTV feed built from multiple US EPGShare sources and published through GitHub Pages.

## EPG Source URL

Copy the full link below and paste it into the **EPG Source URL** field in your player app:

https://vcicio.github.io/US-EPG/merged_epg.xml.gz

## Download Links

Use the links below to access the latest published EPG files:

- [Download merged_epg.xml.gz](https://vcicio.github.io/US-EPG/merged_epg.xml.gz)
- [Download merged_epg.xml](https://vcicio.github.io/US-EPG/merged_epg.xml)
- [View published site](https://vcicio.github.io/US-EPG/)

## Source Feeds Used

- `https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS1.xml.gz`
- `https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz`
- `https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz`

## Build Behavior

This project attempts to download all configured source feeds, validate them, merge the valid XMLTV data, trim programmes to the configured date window, and publish the resulting merged guide.

If one or more sources fail, the build can still continue as long as at least one source succeeds. When that happens, the generated output and the status section below will indicate that the published EPG may be incomplete.

## Published Site

Your GitHub Pages site publishes the generated files from the `site/` folder.

## Current Source Status

<!-- EPG_STATUS_START -->
Last updated: **2026-03-29 22:45:46 UTC**

Programmes kept in latest build: **520086**

Window start: `2026-03-29T22:41:58.568365+00:00`
Window end: `2026-04-08T22:41:58.568365+00:00`

### Source health

| Source | Status | Notes |
|---|---|---|
| `https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS1.xml.gz` | Working |  |
| `https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz` | Working |  |
| `https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz` | Working |  |
| `http://proxpanel.fans:8080/xmltv.php?username=7112221312&password=5268412129` | Failed | download failed: Failed to download valid source after 3 attempts: http://proxpanel.fans:8080/xmltv.php?username=7112221312&password=5268412129 |

### Summary

- Working sources: **3**
- Failed sources: **1**

**Warning:** The latest published EPG may be incomplete because one or more sources failed.

<!-- EPG_STATUS_END -->

## Notes

- The status section above is updated automatically by `scripts/build_epg.py`
- The README is committed automatically by the GitHub Actions workflow
- The generated XML and XML.GZ files are published through GitHub Pages
