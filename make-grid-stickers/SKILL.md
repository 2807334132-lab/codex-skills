---
name: make-grid-stickers
description: Extract characters or sticker subjects from a grid image, remove the plain white background, crop each subject tightly, and export transparent GIF sticker files. Use when the user asks to turn a 3x3, 2x3, or similar multi-character image sheet into individual stickers, emoji packs, reaction images, or GIF stickers.
---

# Make Grid Stickers

## Overview

Use this skill to convert a grid-style character sheet into individual sticker files. It is best for images with a mostly white or plain background and separated subjects, such as 3x3 AI-generated character sheets.

The bundled script performs deterministic local processing:

- detects foreground connected components after removing border-connected white background
- assigns components to the nearest grid cell
- preserves nearby decorations such as hearts, butterflies, sparkles, or petals
- crops each sticker tightly with configurable padding
- exports transparent static GIF files, optional PNG files, a preview contact sheet, and a zip archive

## Workflow

1. Copy or reference the source image using a filesystem path. If the filename has non-ASCII characters and command-line quoting is fragile, copy it to a simple ASCII filename first.
2. Run `scripts/make_grid_stickers.py` with the input image and output directory.
3. Inspect `preview_gif_contact_sheet.jpg`.
4. If the crop is too loose or too tight, rerun with a different `--padding`.
5. If the grid is not 3x3, set `--rows` and `--cols`.
6. Return the output folder and zip file paths to the user.

## Quick Start

```bash
python scripts/make_grid_stickers.py --input input.png --output out/stickers
```

Common options:

```bash
python scripts/make_grid_stickers.py \
  --input input.png \
  --output out/stickers \
  --rows 3 \
  --cols 3 \
  --padding 18 \
  --export-png
```

## Output

The script creates:

- `sticker_01.gif`, `sticker_02.gif`, etc.
- `preview_gif_contact_sheet.jpg`
- `<output-folder-name>.zip`
- optional tight transparent PNG files when `--export-png` is used

## Notes

- GIF only supports one-bit transparency, so antialiased transparent edges are approximated. Keep PNG output when the user needs the cleanest transparent edge.
- For sheets where subjects touch each other or the background is complex, this script may need manual crop coordinates or image editing instead of automatic grid assignment.
- When the user asks for "GIF format" but not animation, export static GIF files.
