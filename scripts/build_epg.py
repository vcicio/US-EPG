import gzip
import shutil
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ===== SETTINGS =====
DAYS_FORWARD = 10

SOURCE_URLS = [
    "https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz",
]

ROOT_DIR = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT_DIR / "work"
SITE_DIR = ROOT_DIR / "site"

OUTPUT_XML_GZ = SITE_DIR / "merged_epg.xml.gz"
OUTPUT_XML = SITE_DIR / "merged_epg.xml"


def parse_xmltv_datetime(dt_str: str) -> datetime:
    dt_str = dt_str.strip()

    if " " in dt_str:
        main_part, offset_part = dt_str.split(" ", 1)
        dt = datetime.strptime(main_part, "%Y%m%d%H%M%S")

        sign = 1 if offset_part[0] == "+" else -1
        offset_hours = int(offset_part[1:3])
        offset_minutes = int(offset_part[3:5])

        tz = timezone(sign * timedelta(hours=offset_hours, minutes=offset_minutes))
        return dt.replace(tzinfo=tz)

    return datetime.strptime(dt_str, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)


def format_xmltv_datetime(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M%S %z")


def download_file(url: str, destination: Path, retries: int = 3, retry_delay: int = 3) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://epgshare01.online/epgshare01/",
    }

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            if destination.exists():
                destination.unlink()

            request = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(request, timeout=60) as response, open(destination, "wb") as out_file:
                shutil.copyfileobj(response, out_file)

            size = destination.stat().st_size
            print(f"Saved {destination.name}: {size} bytes")

            if size == 0:
                raise ValueError(f"Downloaded file is empty from {url}")

            try:
                with gzip.open(destination, "rb") as f:
                    preview_bytes = f.read(512)
            except OSError as e:
                raise ValueError(f"Downloaded file is not a valid gzip from {url}") from e

            if not preview_bytes.strip():
                raise ValueError(f"Gzip content is empty from {url}")

            if not preview_bytes.lstrip().startswith(b"<"):
                preview = preview_bytes[:200].decode("utf-8", errors="replace")
                raise ValueError(
                    f"Downloaded content does not look like XML from {url}. Preview: {preview!r}"
                )

            print(f"Validated download: {url}")
            return

        except Exception as e:
            last_error = e
            print(f"Attempt {attempt}/{retries} failed for {url}: {e}")

            if attempt < retries:
                time.sleep(retry_delay)

    raise RuntimeError(f"Failed to download valid source after {retries} attempts: {url}") from last_error


def load_xmltv_gz(path: Path, source_url: str) -> ET.ElementTree:
    if not path.exists():
        raise FileNotFoundError(f"Missing downloaded file for {source_url}: {path}")

    size = path.stat().st_size
    if size == 0:
        raise ValueError(f"Downloaded file is empty for {source_url}: {path}")

    try:
        with gzip.open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise ValueError(f"Invalid gzip file for {source_url}: {path}") from e

    if not data.strip():
        raise ValueError(f"Decompressed XML is empty for {source_url}: {path}")

    preview = data[:200].decode("utf-8", errors="replace")
    print(f"Preview for {path.name}: {preview[:120]!r}")

    if not data.lstrip().startswith(b"<"):
        raise ValueError(
            f"Content does not appear to be XML for {source_url}: {path}. Preview: {preview!r}"
        )

    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        raise ValueError(
            f"XML parse failed for {source_url}: {path}. Preview: {preview!r}"
        ) from e

    return ET.ElementTree(root)


def save_xmltv(tree: ET.ElementTree, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def save_xmltv_gz(tree: ET.ElementTree, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)


def merge_trees(trees: list[ET.ElementTree]) -> ET.ElementTree:
    if not trees:
        raise ValueError("No XML trees to merge.")

    base_root = trees[0].getroot()

    existing_channel_ids = {
        ch.get("id") for ch in base_root.findall("channel") if ch.get("id")
    }

    existing_programme_keys = set()
    for prog in base_root.findall("programme"):
        key = (
            prog.get("channel"),
            prog.get("start"),
            prog.get("stop"),
            (prog.findtext("title") or "").strip(),
        )
        existing_programme_keys.add(key)

    for tree in trees[1:]:
        root = tree.getroot()

        for channel in root.findall("channel"):
            channel_id = channel.get("id")
            if channel_id and channel_id not in existing_channel_ids:
                base_root.append(channel)
                existing_channel_ids.add(channel_id)

        for programme in root.findall("programme"):
            key = (
                programme.get("channel"),
                programme.get("start"),
                programme.get("stop"),
                (programme.findtext("title") or "").strip(),
            )
            if key not in existing_programme_keys:
                base_root.append(programme)
                existing_programme_keys.add(key)

    return ET.ElementTree(base_root)


def trim_programmes(root: ET.Element, days_forward: int) -> tuple[int, str, str]:
    now = datetime.now().astimezone()
    cutoff = now + timedelta(days=days_forward)

    all_programmes = root.findall("programme")
    kept_programmes = []

    for programme in all_programmes:
        start_raw = programme.get("start")
        stop_raw = programme.get("stop")

        if not start_raw or not stop_raw:
            continue

        try:
            start_dt = parse_xmltv_datetime(start_raw).astimezone(now.tzinfo)
            stop_dt = parse_xmltv_datetime(stop_raw).astimezone(now.tzinfo)
        except Exception:
            continue

        if stop_dt <= now:
            continue

        if start_dt >= cutoff:
            continue

        if stop_dt > cutoff:
            programme.set("stop", format_xmltv_datetime(cutoff))

        kept_programmes.append(programme)

    for programme in all_programmes:
        root.remove(programme)

    for programme in kept_programmes:
        root.append(programme)

    return (
        len(kept_programmes),
        now.isoformat(),
        cutoff.isoformat(),
    )


def write_index_html(programmes_kept: int, window_start: str, window_end: str) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>US-EPG</title>
</head>
<body>
  <h1>US-EPG</h1>
  <p>This feed is auto-generated from:</p>
  <ul>
    <li>epg_ripper_US_LOCALS1.xml.gz</li>
    <li>epg_ripper_US2.xml.gz</li>
    <li>epg_ripper_US_SPORTS1.xml.gz</li>
  </ul>
  <p><a href="merged_epg.xml.gz">Download merged_epg.xml.gz</a></p>
  <p><a href="merged_epg.xml">Download merged_epg.xml</a></p>
  <p>Programmes kept: {programmes_kept}</p>
  <p>Window start: {window_start}</p>
  <p>Window end: {window_end}</p>
</body>
</html>
"""
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")


def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_files: list[tuple[str, Path]] = []

    for i, url in enumerate(SOURCE_URLS, start=1):
        local_path = WORK_DIR / f"source_{i}.xml.gz"
        print(f"Downloading source_{i}: {url}")
        download_file(url, local_path)
        downloaded_files.append((url, local_path))

    trees = []
    for url, path in downloaded_files:
        print(f"Parsing {path.name} from {url}")
        tree = load_xmltv_gz(path, url)
        trees.append(tree)

    if len(trees) != len(SOURCE_URLS):
        raise RuntimeError(
            f"Expected {len(SOURCE_URLS)} essential sources, but only parsed {len(trees)}."
        )

    merged_tree = merge_trees(trees)
    merged_root = merged_tree.getroot()

    kept_count, window_start, window_end = trim_programmes(merged_root, DAYS_FORWARD)

    save_xmltv(merged_tree, OUTPUT_XML)
    save_xmltv_gz(merged_tree, OUTPUT_XML_GZ)
    write_index_html(kept_count, window_start, window_end)

    print("Finished.")
    print(f"Saved XML: {OUTPUT_XML}")
    print(f"Saved XML.GZ: {OUTPUT_XML_GZ}")
    print(f"Programmes kept: {kept_count}")
    print(f"Window start: {window_start}")
    print(f"Window end: {window_end}")


if __name__ == "__main__":
    main()
        tz = timezone(sign * timedelta(hours=offset_hours, minutes=offset_minutes))
        return dt.replace(tzinfo=tz)

    return datetime.strptime(dt_str, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)


def format_xmltv_datetime(dt: datetime) -> str:
    return dt.strftime("%Y%m%d%H%M%S %z")


def download_file(url: str, destination: Path, retries: int = 3, retry_delay: int = 3) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://epgshare01.online/epgshare01/",
    }

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            if destination.exists():
                destination.unlink()

            request = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(request, timeout=60) as response, open(destination, "wb") as out_file:
                shutil.copyfileobj(response, out_file)

            size = destination.stat().st_size
            print(f"Saved {destination.name}: {size} bytes")

            if size == 0:
                raise ValueError(f"Downloaded file is empty from {url}")

            # Validate that it is actually readable as gzip and contains some data
            with gzip.open(destination, "rb") as f:
                preview_bytes = f.read(512)

            if not preview_bytes.strip():
                raise ValueError(f"Gzip content is empty from {url}")

            if not preview_bytes.lstrip().startswith(b"<"):
                preview = preview_bytes[:200].decode("utf-8", errors="replace")
                raise ValueError(
                    f"Downloaded content does not look like XML from {url}. Preview: {preview!r}"
                )

            return

        except Exception as e:
            last_error = e
            print(f"Attempt {attempt}/{retries} failed for {url}: {e}")

            if attempt < retries:
                time.sleep(retry_delay)

    raise RuntimeError(f"Failed to download valid source after {retries} attempts: {url}") from last_error


def load_xmltv_gz(path: Path, source_url: str) -> ET.ElementTree:
    if not path.exists():
        raise FileNotFoundError(f"Missing downloaded file for {source_url}: {path}")

    size = path.stat().st_size
    if size == 0:
        raise ValueError(f"Downloaded file is empty for {source_url}: {path}")

    try:
        with gzip.open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise ValueError(f"Invalid gzip file for {source_url}: {path}") from e

    if not data.strip():
        raise ValueError(f"Decompressed XML is empty for {source_url}: {path}")

    preview = data[:200].decode("utf-8", errors="replace")
    print(f"Preview for {path.name}: {preview[:120]!r}")

    if not data.lstrip().startswith(b"<"):
        raise ValueError(
            f"Content does not appear to be XML for {source_url}: {path}. Preview: {preview!r}"
        )

    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        raise ValueError(
            f"XML parse failed for {source_url}: {path}. Preview: {preview!r}"
        ) from e

    return ET.ElementTree(root)


def save_xmltv(tree: ET.ElementTree, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def save_xmltv_gz(tree: ET.ElementTree, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)


def merge_trees(trees: list[ET.ElementTree]) -> ET.ElementTree:
    if not trees:
        raise ValueError("No XML trees to merge.")

    base_root = trees[0].getroot()

    existing_channel_ids = {
        ch.get("id") for ch in base_root.findall("channel") if ch.get("id")
    }

    existing_programme_keys = set()
    for prog in base_root.findall("programme"):
        key = (
            prog.get("channel"),
            prog.get("start"),
            prog.get("stop"),
            (prog.findtext("title") or "").strip(),
        )
        existing_programme_keys.add(key)

    for tree in trees[1:]:
        root = tree.getroot()

        for channel in root.findall("channel"):
            channel_id = channel.get("id")
            if channel_id and channel_id not in existing_channel_ids:
                base_root.append(channel)
                existing_channel_ids.add(channel_id)

        for programme in root.findall("programme"):
            key = (
                programme.get("channel"),
                programme.get("start"),
                programme.get("stop"),
                (programme.findtext("title") or "").strip(),
            )
            if key not in existing_programme_keys:
                base_root.append(programme)
                existing_programme_keys.add(key)

    return ET.ElementTree(base_root)


def trim_programmes(root: ET.Element, days_forward: int) -> tuple[int, str, str]:
    now = datetime.now().astimezone()
    cutoff = now + timedelta(days=days_forward)

    all_programmes = root.findall("programme")
    kept_programmes = []

    for programme in all_programmes:
        start_raw = programme.get("start")
        stop_raw = programme.get("stop")

        if not start_raw or not stop_raw:
            continue

        try:
            start_dt = parse_xmltv_datetime(start_raw).astimezone(now.tzinfo)
            stop_dt = parse_xmltv_datetime(stop_raw).astimezone(now.tzinfo)
        except Exception:
            continue

        if stop_dt <= now:
            continue

        if start_dt >= cutoff:
            continue

        if stop_dt > cutoff:
            programme.set("stop", format_xmltv_datetime(cutoff))

        kept_programmes.append(programme)

    for programme in all_programmes:
        root.remove(programme)

    for programme in kept_programmes:
        root.append(programme)

    return (
        len(kept_programmes),
        now.isoformat(),
        cutoff.isoformat(),
    )


def write_index_html(programmes_kept: int, window_start: str, window_end: str) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>US-EPG</title>
</head>
<body>
  <h1>US-EPG</h1>
  <p>This feed is auto-generated from:</p>
  <ul>
    <li>epg_ripper_US_LOCALS1.xml.gz</li>
    <li>epg_ripper_US2.xml.gz</li>
    <li>epg_ripper_US_SPORTS1.xml.gz</li>
  </ul>
  <p><a href="merged_epg.xml.gz">Download merged_epg.xml.gz</a></p>
  <p><a href="merged_epg.xml">Download merged_epg.xml</a></p>
  <p>Programmes kept: {programmes_kept}</p>
  <p>Window start: {window_start}</p>
  <p>Window end: {window_end}</p>
</body>
</html>
"""
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")


def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_files = []

    for i, url in enumerate(SOURCE_URLS, start=1):
        local_path = WORK_DIR / f"source_{i}.xml.gz"
        print(f"Downloading source_{i}: {url}")
        download_file(url, local_path)
        downloaded_files.append((url, local_path))

    trees = []
    for url, path in downloaded_files:
        print(f"Parsing {path.name} from {url}")
        tree = load_xmltv_gz(path, url)
        trees.append(tree)

    if len(trees) != len(SOURCE_URLS):
        raise RuntimeError(
            f"Expected {len(SOURCE_URLS)} essential sources, but only parsed {len(trees)}."
        )

    merged_tree = merge_trees(trees)
    merged_root = merged_tree.getroot()

    kept_count, window_start, window_end = trim_programmes(merged_root, DAYS_FORWARD)

    save_xmltv(merged_tree, OUTPUT_XML)
    save_xmltv_gz(merged_tree, OUTPUT_XML_GZ)
    write_index_html(kept_count, window_start, window_end)

    print("Finished.")
    print(f"Saved XML: {OUTPUT_XML}")
    print(f"Saved XML.GZ: {OUTPUT_XML_GZ}")
    print(f"Programmes kept: {kept_count}")
    print(f"Window start: {window_start}")
    print(f"Window end: {window_end}")


if __name__ == "__main__":
    main()
