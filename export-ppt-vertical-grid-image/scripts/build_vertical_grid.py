from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


def parse_ratio(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)\s*:\s*(\d+)", value)
    if not match:
        raise argparse.ArgumentTypeError("ratio must look like 3:4")
    width, height = map(int, match.groups())
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("ratio values must be positive")
    return width, height


def discover_slides(folder: Path) -> dict[int, Path]:
    found: dict[int, Path] = {}
    for path in folder.iterdir():
        if path.suffix.lower() != ".png":
            continue
        match = re.search(r"(\d+)(?=\D*$)", path.stem)
        if match:
            found[int(match.group(1))] = path
    if not found:
        raise FileNotFoundError(f"No numbered PNG slides found in {folder}")
    return found


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def fit_slide(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        return image.convert("RGB").resize(size, Image.Resampling.LANCZOS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a cover-plus-grid vertical PPT overview image.")
    parser.add_argument("--slides-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ratio", type=parse_ratio, default=(3, 4))
    parser.add_argument("--width", type=int, default=1800)
    parser.add_argument("--cover", type=int, default=1)
    parser.add_argument("--grid-start", type=int, default=2)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--closing-slide", type=int)
    parser.add_argument("--main-text", default="")
    parser.add_argument("--sub-text", default="")
    parser.add_argument("--margin", type=int, default=8)
    parser.add_argument("--gap", type=int, default=8)
    args = parser.parse_args()

    ratio_w, ratio_h = args.ratio
    height = round(args.width * ratio_h / ratio_w)
    slides = discover_slides(args.slides_dir)
    required = [args.cover] + list(range(args.grid_start, args.grid_start + args.rows * args.cols))
    missing = [number for number in required if number not in slides]
    if missing:
        raise FileNotFoundError(f"Missing slide renders: {missing}")

    background = (244, 247, 252)
    canvas = Image.new("RGB", (args.width, height), background)
    content_width = args.width - args.margin * 2

    cover_height = round(content_width * 9 / 16)
    cover = fit_slide(slides[args.cover], (content_width, cover_height))
    canvas.paste(cover, (args.margin, args.margin))

    grid_y = args.margin + cover_height + args.gap
    available_width = content_width - args.gap * (args.cols - 1)
    base_width = available_width // args.cols
    widths = [base_width] * args.cols
    widths[-1] += available_width - sum(widths)
    tile_height = min(round(width * 9 / 16) for width in widths)

    slide_number = args.grid_start
    y = grid_y
    for _row in range(args.rows):
        x = args.margin
        for col in range(args.cols):
            tile = fit_slide(slides[slide_number], (widths[col], tile_height))
            canvas.paste(tile, (x, y))
            x += widths[col] + args.gap
            slide_number += 1
        y += tile_height + args.gap

    footer_y = y
    footer_height = height - args.margin - footer_y
    if footer_height < 0:
        raise ValueError("The cover and grid do not fit the requested canvas ratio.")

    if footer_height > 0:
        closing_number = args.closing_slide or max(slides)
        if closing_number not in slides:
            raise FileNotFoundError(f"Missing closing slide render: {closing_number}")
        with Image.open(slides[closing_number]) as source:
            footer = ImageOps.fit(
                source.convert("RGB"),
                (content_width, footer_height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.72),
            )
        footer = ImageEnhance.Contrast(footer).enhance(1.03)
        navy = Image.new("RGB", footer.size, (5, 43, 95))
        footer = Image.blend(footer, navy, 0.68)

        draw = ImageDraw.Draw(footer)
        if args.main_text:
            main_font = load_font(max(30, round(args.width * 0.036)), bold=True)
            box = draw.textbbox((0, 0), args.main_text, font=main_font)
            x = (content_width - (box[2] - box[0])) // 2
            draw.text((x, round(footer_height * 0.23)), args.main_text, font=main_font, fill=(255, 255, 255))
        if args.sub_text:
            sub_font = load_font(max(18, round(args.width * 0.017)), bold=False)
            box = draw.textbbox((0, 0), args.sub_text, font=sub_font)
            x = (content_width - (box[2] - box[0])) // 2
            draw.text((x, round(footer_height * 0.56)), args.sub_text, font=sub_font, fill=(255, 218, 143))
        canvas.paste(footer, (args.margin, footer_y))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    suffix = args.output.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        canvas.save(args.output, "JPEG", quality=95, subsampling=0, optimize=True, dpi=(150, 150))
    elif suffix == ".png":
        canvas.save(args.output, "PNG", optimize=True, dpi=(150, 150))
    else:
        raise ValueError("Output must be .jpg, .jpeg, or .png")

    with Image.open(args.output) as result:
        expected_height = round(result.width * ratio_h / ratio_w)
        if result.height != expected_height:
            raise RuntimeError(f"Output ratio check failed: {result.size}")
    print(f"Created {args.output} ({args.width}x{height})")


if __name__ == "__main__":
    main()
