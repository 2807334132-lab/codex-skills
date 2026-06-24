#!/usr/bin/env python3
"""Convert raster images to pixel-exact and/or traced SVG files."""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys

try:
    from PIL import Image
except Exception as exc:  # pragma: no cover
    raise SystemExit("Pillow is required to run this script") from exc


def hex_color(rgb):
    return "#%02x%02x%02x" % rgb


def load_rgb(path: Path):
    image = Image.open(path).convert("RGB")
    return image, image.size


def write_pixel_exact(image: Image.Image, out_path: Path) -> None:
    width, height = image.size
    pix = image.load()
    runs_by_color = defaultdict(list)

    for y in range(height):
        x = 0
        while x < width:
            color = pix[x, y]
            x2 = x + 1
            while x2 < width and pix[x2, y] == color:
                x2 += 1
            run_width = x2 - x
            runs_by_color[color].append(f"M{x} {y}h{run_width}v1h-{run_width}z")
            x = x2

    items = sorted(runs_by_color.items(), key=lambda item: len(item[1]), reverse=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" shape-rendering="crispEdges" '
            f'role="img" aria-labelledby="title desc">\n'
        )
        f.write('<title id="title">Pixel-perfect vectorized image</title>\n')
        f.write('<desc id="desc">Each source pixel run is represented as SVG vector path rectangles.</desc>\n')
        for color, runs in items:
            f.write(f'<path fill="{hex_color(color)}" d="')
            f.write("".join(runs))
            f.write('"/>\n')
        f.write("</svg>\n")


def write_trace(image: Image.Image, out_path: Path, threshold: int) -> None:
    local_deps = Path.cwd() / ".codex_pydeps"
    if local_deps.exists() and str(local_deps) not in sys.path:
        sys.path.insert(0, str(local_deps))

    try:
        import cv2
        import numpy as np
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "OpenCV and numpy are required for --mode trace. "
            "Install opencv-python-headless or rerun with --mode pixel."
        ) from exc

    width, height = image.size
    arr = np.array(image)
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    mask = (((sat > threshold) & (val < 254)) | (val < 245)).astype(np.uint8) * 255
    mask = cv2.medianBlur(mask, 3)

    contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda c: cv2.contourArea(c), reverse=True)
    parts = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 2:
            continue
        approx = cv2.approxPolyDP(contour, 0.55, True)
        pts = approx.reshape(-1, 2)
        if len(pts) < 3:
            continue
        d = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
        d.extend(f"L{x:.1f},{y:.1f}" for x, y in pts[1:])
        d.append("Z")
        parts.append(" ".join(d))

    foreground = arr[mask > 0]
    fill = "#d00055"
    if len(foreground):
        mean = foreground.mean(axis=0).astype(int)
        fill = hex_color(tuple(int(v) for v in mean))

    with out_path.open("w", encoding="utf-8", newline="") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" aria-labelledby="title desc">\n'
        )
        f.write('<title id="title">Editable traced vector image</title>\n')
        f.write('<desc id="desc">Foreground contours traced from the source raster image.</desc>\n')
        f.write('<rect width="100%" height="100%" fill="#fff"/>\n')
        f.write(f'<path d="{" ".join(parts)}" fill="{fill}" fill-rule="evenodd"/>\n')
        f.write("</svg>\n")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source PNG/JPG image")
    parser.add_argument("--out-dir", type=Path, default=Path.cwd(), help="Directory for SVG outputs")
    parser.add_argument("--base-name", default=None, help="Output base name; defaults to source stem")
    parser.add_argument("--mode", choices=("pixel", "trace", "both"), default="both")
    parser.add_argument("--threshold", type=int, default=28, help="Saturation threshold for trace foreground detection")
    args = parser.parse_args(argv)

    image, _ = load_rgb(args.input)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    base = args.base_name or args.input.stem
    outputs = []

    if args.mode in ("pixel", "both"):
        out = args.out_dir / f"{base}_pixel_exact.svg"
        write_pixel_exact(image, out)
        outputs.append(out)

    if args.mode in ("trace", "both"):
        out = args.out_dir / f"{base}_trace.svg"
        write_trace(image, out, args.threshold)
        outputs.append(out)

    for out in outputs:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
