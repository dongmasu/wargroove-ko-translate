#!/usr/bin/env python3
"""Pack the Wargroove 2 workspaces into a dated distributable ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import datetime
from pathlib import Path

from config_workspace import pack_workspace


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VERSION = "1.2.x"
DEFAULT_WORK = ROOT / "work/Wargroove 2"
DEFAULT_DIST = ROOT / "dist/Wargroove 2"
ARCHIVE_PREFIX = "Wargroove2-ko-translate"


def latest_work_date(work_root: Path) -> tuple[str, str]:
    files = [path for path in work_root.rglob("*") if path.is_file()]
    if not files:
        raise ValueError(f"work directory is empty: {work_root}")
    latest = max(files, key=lambda path: path.stat().st_mtime)
    timestamp = datetime.fromtimestamp(latest.stat().st_mtime)
    return timestamp.strftime("%Y%m%d"), str(latest)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build(
    version: str,
    work_root: Path,
    dist_root: Path,
    date_override: str | None = None,
) -> dict[str, object]:
    version_root = work_root / version
    config_workspace = version_root / "config"
    ui_workspace = version_root / "ui"
    if not (config_workspace / "workspace.json").is_file():
        raise ValueError(f"config workspace is missing: {config_workspace}")
    if not (ui_workspace / "workspace.json").is_file():
        raise ValueError(f"ui workspace is missing: {ui_workspace}")

    release_date, latest_file = latest_work_date(version_root)
    if date_override is not None:
        if len(date_override) != 8 or not date_override.isdigit():
            raise ValueError("--date must use YYYYMMDD")
        release_date = date_override

    release_root = dist_root / version / release_date
    assets_root = release_root / "assets"
    config_output = assets_root / "config.dat"
    ui_output = assets_root / "ui.dat"
    archive = release_root / f"{ARCHIVE_PREFIX}-{version}-{release_date}.zip"
    outputs = (config_output, ui_output, archive)
    existing = [str(path) for path in outputs if path.exists()]
    if existing:
        raise FileExistsError(
            "refusing to overwrite existing release files: " + ", ".join(existing)
        )

    config_result = pack_workspace(config_workspace, config_output)
    ui_result = pack_workspace(ui_workspace, ui_output)

    # config_workspace writes sidecar reports; the distributable contains DATs only.
    for sidecar in (config_output.with_suffix(".json"), ui_output.with_suffix(".json")):
        sidecar.unlink(missing_ok=True)

    with zipfile.ZipFile(
        archive,
        "x",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as bundle:
        bundle.write(config_output, "assets/config.dat")
        bundle.write(ui_output, "assets/ui.dat")

    return {
        "version": version,
        "date": release_date,
        "latest_work_file": latest_file,
        "config": config_result,
        "ui": ui_result,
        "archive": str(archive),
        "archive_sha256": sha256(archive),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--work-root", type=Path, default=DEFAULT_WORK)
    parser.add_argument("--dist-root", type=Path, default=DEFAULT_DIST)
    parser.add_argument(
        "--date",
        help="override the date (YYYYMMDD); default is the latest work-file date",
    )
    args = parser.parse_args()
    try:
        result = build(args.version, args.work_root, args.dist_root, args.date)
    except (FileExistsError, OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
