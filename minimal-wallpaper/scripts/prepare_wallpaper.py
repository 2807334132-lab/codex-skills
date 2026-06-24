#!/usr/bin/env python3
"""Crop/resize an image for a Windows desktop wallpaper and optionally set it."""

from __future__ import annotations

import argparse
import ctypes
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image


SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


def crop_cover(img: Image.Image, width: int, height: int) -> Image.Image:
    source_width, source_height = img.size
    source_ratio = source_width / source_height
    target_ratio = width / height

    if source_ratio > target_ratio:
        new_width = int(source_height * target_ratio)
        left = (source_width - new_width) // 2
        img = img.crop((left, 0, left + new_width, source_height))
    elif source_ratio < target_ratio:
        new_height = int(source_width / target_ratio)
        top = (source_height - new_height) // 2
        img = img.crop((0, top, source_width, top + new_height))

    return img.resize((width, height), Image.Resampling.LANCZOS)


def set_wallpaper(path: Path) -> None:
    absolute = str(path.resolve())
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            (
                "Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' "
                "-Name WallpaperStyle -Value '10'; "
                "Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' "
                "-Name TileWallpaper -Value '0'"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    ok = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        absolute,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
    )
    if not ok:
        raise RuntimeError("Windows did not accept the wallpaper path.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a screen-sized Windows wallpaper.")
    parser.add_argument("--input", required=True, help="Generated source image")
    parser.add_argument("--output", required=True, help="Final wallpaper image path")
    parser.add_argument("--width", type=int, required=True, help="Target screen width")
    parser.add_argument("--height", type=int, required=True, help="Target screen height")
    parser.add_argument("--set", action="store_true", help="Set the output image as wallpaper")
    parser.add_argument("--copy-original-to", help="Optional stable copy path for the uncropped original")
    args = parser.parse_args()

    source = Path(args.input).resolve()
    output = Path(args.output).resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)

    if args.copy_original_to:
        original_copy = Path(args.copy_original_to).resolve()
        original_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, original_copy)
    else:
        original_copy = None

    image = Image.open(source).convert("RGB")
    wallpaper = crop_cover(image, args.width, args.height)
    wallpaper.save(output, quality=95)

    if args.set:
        set_wallpaper(output)

    print(
        json.dumps(
            {
                "output": str(output),
                "width": args.width,
                "height": args.height,
                "bytes": output.stat().st_size,
                "set": bool(args.set),
                "original_copy": str(original_copy) if original_copy else None,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
