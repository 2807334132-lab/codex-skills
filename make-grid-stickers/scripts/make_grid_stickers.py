#!/usr/bin/env python3
"""Extract tight transparent GIF stickers from a grid-style image sheet."""

from __future__ import annotations

import argparse
import zipfile
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter


def is_background(pixel: tuple[int, int, int, int], threshold: int, tolerance: int) -> bool:
    r, g, b, a = pixel
    return a == 0 or (
        a > 0
        and r >= threshold
        and g >= threshold
        and b >= threshold
        and max(r, g, b) - min(r, g, b) <= tolerance
    )


def remove_border_background(image: Image.Image, threshold: int, tolerance: int) -> Image.Image:
    image = image.convert("RGBA")
    width, height = image.size
    pixels = image.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def push(x: int, y: int) -> None:
        idx = y * width + x
        if not visited[idx] and is_background(pixels[x, y], threshold, tolerance):
            visited[idx] = 1
            queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        pixels[x, y] = (255, 255, 255, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height:
                push(nx, ny)

    return image


def find_components(image: Image.Image, min_area: int) -> list[dict]:
    alpha = image.getchannel("A")
    width, height = image.size
    alpha_pixels = alpha.load()
    seen = bytearray(width * height)
    components = []

    for y in range(height):
        for x in range(width):
            idx = y * width + x
            if seen[idx] or alpha_pixels[x, y] == 0:
                continue

            seen[idx] = 1
            queue: deque[tuple[int, int]] = deque([(x, y)])
            xs: list[int] = []
            ys: list[int] = []
            component_pixels: list[tuple[int, int]] = []

            while queue:
                cx, cy = queue.popleft()
                xs.append(cx)
                ys.append(cy)
                component_pixels.append((cx, cy))

                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < width and 0 <= ny < height:
                        neighbor_idx = ny * width + nx
                        if not seen[neighbor_idx] and alpha_pixels[nx, ny] > 0:
                            seen[neighbor_idx] = 1
                            queue.append((nx, ny))

            if len(component_pixels) >= min_area:
                components.append(
                    {
                        "pixels": component_pixels,
                        "area": len(component_pixels),
                        "bbox": (min(xs), min(ys), max(xs) + 1, max(ys) + 1),
                        "centroid": (sum(xs) / len(xs), sum(ys) / len(ys)),
                    }
                )

    return components


def assign_components(components: list[dict], width: int, height: int, rows: int, cols: int) -> list[list[dict]]:
    centers = [((col + 0.5) * width / cols, (row + 0.5) * height / rows) for row in range(rows) for col in range(cols)]
    assigned: list[list[dict]] = [[] for _ in range(rows * cols)]

    for component in components:
        cx, cy = component["centroid"]
        index = min(range(len(centers)), key=lambda i: (cx - centers[i][0]) ** 2 + (cy - centers[i][1]) ** 2)
        assigned[index].append(component)

    return assigned


def make_component_mask(
    image: Image.Image,
    components: list[dict],
    large_area: int,
    decoration_margin: int,
) -> Image.Image | None:
    if not components:
        return None

    alpha = image.getchannel("A")
    alpha_pixels = alpha.load()
    width, height = image.size
    large = [component for component in components if component["area"] >= large_area] or components

    lx1 = min(component["bbox"][0] for component in large)
    ly1 = min(component["bbox"][1] for component in large)
    lx2 = max(component["bbox"][2] for component in large)
    ly2 = max(component["bbox"][3] for component in large)

    kept = []
    for component in components:
        ccx, ccy = component["centroid"]
        near_main_subject = lx1 - decoration_margin <= ccx <= lx2 + decoration_margin and ly1 - decoration_margin <= ccy <= ly2 + decoration_margin
        if component["area"] >= 24 or near_main_subject:
            kept.append(component)

    if not kept:
        return None

    mask = Image.new("L", (width, height), 0)
    mask_pixels = mask.load()
    for component in kept:
        for x, y in component["pixels"]:
            mask_pixels[x, y] = alpha_pixels[x, y]

    return mask


def add_white_outline(image: Image.Image, radius: int) -> Image.Image:
    if radius <= 0:
        return image

    alpha = image.getchannel("A")
    outline = alpha.filter(ImageFilter.MaxFilter(radius * 2 + 1)).filter(ImageFilter.GaussianBlur(1.0))
    base = Image.new("RGBA", image.size, (255, 255, 255, 0))
    base.paste(Image.new("RGBA", image.size, (255, 255, 255, 255)), mask=outline)
    base.alpha_composite(image)
    return base


def crop_with_padding(image: Image.Image, padding: int) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return image

    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)
    return image.crop((left, top, right, bottom))


def rgba_to_transparent_gif(image: Image.Image, path: Path) -> None:
    alpha = image.getchannel("A")
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    composed = Image.alpha_composite(background, image)
    composed.putalpha(alpha.point(lambda a: 0 if a < 8 else 255, "L"))

    paletted = composed.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    palette = paletted.getpalette() or []
    if len(palette) < 768:
        palette += [0] * (768 - len(palette))
    palette[255 * 3 : 255 * 3 + 3] = [255, 0, 255]
    paletted.putpalette(palette)

    transparent_mask = composed.getchannel("A").point(lambda a: 255 if a == 0 else 0, "1")
    paletted.paste(255, mask=transparent_mask)
    paletted.save(path, save_all=False, transparency=255, disposal=2)


def make_preview(gif_paths: list[Path], path: Path, cols: int = 3, tile_size: int = 220) -> None:
    rows = (len(gif_paths) + cols - 1) // cols
    sheet = Image.new("RGB", (tile_size * cols, tile_size * rows), (245, 245, 245))

    for index, gif_path in enumerate(gif_paths):
        image = Image.open(gif_path).convert("RGBA")
        scale = min((tile_size - 20) / image.width, (tile_size - 20) / image.height)
        resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", (tile_size, tile_size), (245, 245, 245, 255))
        tile.alpha_composite(resized, ((tile_size - resized.width) // 2, (tile_size - resized.height) // 2))
        sheet.paste(tile.convert("RGB"), ((index % cols) * tile_size, (index // cols) * tile_size))

    sheet.save(path, quality=92)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract grid image subjects into tight GIF stickers.")
    parser.add_argument("--input", required=True, type=Path, help="Source grid image.")
    parser.add_argument("--output", required=True, type=Path, help="Output folder.")
    parser.add_argument("--rows", type=int, default=3, help="Grid row count.")
    parser.add_argument("--cols", type=int, default=3, help="Grid column count.")
    parser.add_argument("--padding", type=int, default=18, help="Transparent padding around the tight crop.")
    parser.add_argument("--outline", type=int, default=8, help="White sticker outline radius in pixels. Use 0 to disable.")
    parser.add_argument("--white-threshold", type=int, default=246, help="Minimum RGB value considered white background.")
    parser.add_argument("--white-tolerance", type=int, default=12, help="Maximum RGB channel spread considered white/neutral.")
    parser.add_argument("--min-component-area", type=int, default=6, help="Ignore foreground specks smaller than this area.")
    parser.add_argument("--large-component-area", type=int, default=80, help="Area used to identify main subject components.")
    parser.add_argument("--decoration-margin", type=int, default=90, help="Keep small decorations this close to the main subject.")
    parser.add_argument("--export-png", action="store_true", help="Also export tight transparent PNG stickers.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    source = Image.open(args.input).convert("RGBA")
    foreground = remove_border_background(source, args.white_threshold, args.white_tolerance)
    width, height = foreground.size
    components = find_components(foreground, args.min_component_area)
    assigned = assign_components(components, width, height, args.rows, args.cols)

    gif_paths: list[Path] = []
    png_paths: list[Path] = []

    for index, cell_components in enumerate(assigned, start=1):
        mask = make_component_mask(foreground, cell_components, args.large_component_area, args.decoration_margin)
        if mask is None:
            continue

        bbox = mask.getbbox()
        if bbox is None:
            continue

        sticker = Image.new("RGBA", foreground.size, (255, 255, 255, 0))
        sticker.paste(foreground, (0, 0), mask)
        sticker = sticker.crop(bbox)
        sticker = add_white_outline(sticker, args.outline)
        sticker = crop_with_padding(sticker, args.padding)

        stem = f"sticker_{index:02d}"
        gif_path = args.output / f"{stem}.gif"
        rgba_to_transparent_gif(sticker, gif_path)
        gif_paths.append(gif_path)

        if args.export_png:
            png_path = args.output / f"{stem}.png"
            sticker.save(png_path)
            png_paths.append(png_path)

    preview_path = args.output / "preview_gif_contact_sheet.jpg"
    make_preview(gif_paths, preview_path, cols=min(args.cols, 4))

    zip_path = args.output.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for output_path in [*gif_paths, *png_paths, preview_path]:
            archive.write(output_path, output_path.name)

    print(f"Created {len(gif_paths)} GIF stickers")
    print(f"Output folder: {args.output}")
    print(f"Preview: {preview_path}")
    print(f"Zip: {zip_path}")


if __name__ == "__main__":
    main()
