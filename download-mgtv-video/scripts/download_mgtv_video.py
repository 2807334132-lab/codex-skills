#!/usr/bin/env python
"""Download an MGTV/MangoTV page and normalize the result to a standard MP4."""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import time


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def ensure_module(import_name: str, package_name: str) -> None:
    if importlib.util.find_spec(import_name):
        return
    run([sys.executable, "-m", "pip", "install", "--user", package_name])


def is_standard_mp4(path: Path) -> bool:
    try:
        header = path.read_bytes()[:64].decode("latin1", errors="ignore")
    except OSError:
        return False
    return "ftyp" in header


def newest_video_file(output_dir: Path, start_time: float) -> Path:
    candidates = []
    for path in output_dir.iterdir():
        if path.is_file() and path.suffix.lower() in {".mp4", ".m4v", ".ts"}:
            if path.stat().st_mtime >= start_time - 1:
                candidates.append(path)
    if not candidates:
        raise FileNotFoundError("No downloaded video file was found.")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def remux_to_mp4(source: Path, ffmpeg_exe: str, keep_raw: bool) -> Path:
    target = source.with_suffix(".standard.mp4")
    run([ffmpeg_exe, "-y", "-i", str(source), "-c", "copy", "-movflags", "+faststart", str(target)])

    final = source.with_suffix(".mp4")
    raw_backup = source.with_suffix(".raw.ts")
    if source.resolve() != raw_backup.resolve():
        if raw_backup.exists():
            raw_backup.unlink()
        source.replace(raw_backup)
    if final.exists():
        final.unlink()
    target.replace(final)
    if not keep_raw and raw_backup.exists():
        raw_backup.unlink()
    return final


def main() -> int:
    parser = argparse.ArgumentParser(description="Download an MGTV/MangoTV video page as standard MP4.")
    parser.add_argument("url", help="MGTV video page URL.")
    parser.add_argument("--output-dir", default=".", help="Folder for the downloaded file.")
    parser.add_argument("--format", default="best", help="yt-dlp format selector, e.g. 1358 or best[height<=720]/best.")
    parser.add_argument("--name", help="Optional base filename without extension.")
    parser.add_argument("--keep-raw", action="store_true", help="Keep the raw HLS/MPEG-TS backup after remux.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    ensure_module("yt_dlp", "yt-dlp")
    ensure_module("imageio_ffmpeg", "imageio-ffmpeg")

    import imageio_ffmpeg

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = str(Path(ffmpeg_exe).parent)
    template = f"{args.name}.%(ext)s" if args.name else "%(title).120B-%(id)s.%(ext)s"

    start_time = time.time()
    run(
        [
            sys.executable,
            "-m",
            "yt_dlp",
            "--no-warnings",
            "--restrict-filenames",
            "--ffmpeg-location",
            ffmpeg_dir,
            "-f",
            args.format,
            "-o",
            template,
            args.url,
        ],
        cwd=output_dir,
    )

    downloaded = newest_video_file(output_dir, start_time)
    final = downloaded
    if final.suffix.lower() != ".mp4" or not is_standard_mp4(final):
        final = remux_to_mp4(downloaded, ffmpeg_exe, args.keep_raw)

    if not is_standard_mp4(final):
        raise RuntimeError(f"Output is not a standard MP4: {final}")

    print(f"FINAL_MP4={final}")
    print(f"SIZE_BYTES={final.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
