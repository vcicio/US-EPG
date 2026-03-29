# US-EPG

A custom merged XMLTV feed built from multiple US EPGShare sources and published through GitHub Pages.

## Downloads

- [merged_epg.xml.gz](./site/merged_epg.xml.gz)
- [merged_epg.xml](./site/merged_epg.xml)

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
<!-- EPG_STATUS_END -->

## Notes

- The status section above is updated automatically by `scripts/build_epg.py`
- The README is committed automatically by the GitHub Actions workflow
- The generated XML and XML.GZ files are published through GitHub Pages
