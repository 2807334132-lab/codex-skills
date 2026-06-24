---
name: pixel-perfect-svg
description: Convert reference raster images, especially logos or generated PNG mockups, into SVG vectors when the user asks for a visually identical vector, pixel-perfect SVG, exact PNG-to-SVG conversion, or a lighter editable traced SVG. Use for tasks like "make this image an AI vector", "must be completely identical", "trace this PNG as SVG", or producing both exact and editable vector deliverables from a source PNG/JPG.
---

# Pixel Perfect SVG

## Workflow

1. Inspect the source image dimensions and mode first. Preserve the source aspect ratio and use the original pixel dimensions as the SVG viewBox unless the user asks otherwise.
2. Clarify the meaning of "vector" through outputs, not debate: provide a pixel-perfect SVG for exact visual matching and a traced SVG for editing when possible.
3. Run `scripts/vectorize_image.py` from this skill for deterministic conversion.
4. Name outputs clearly:
   - `*_pixel_exact.svg` for native-size visual identity. This represents pixel runs as vector paths and may be large.
   - `*_trace.svg` for editable contours. This is lighter but not guaranteed to be pixel-identical.
5. Tell the user the tradeoff plainly: pixel-perfect means visually exact at native size but not convenient to edit; traced means editable and scalable but approximate.

## Quick Start

Use the bundled script with the Codex workspace Python when available:

```powershell
& '<python.exe>' '<skill-dir>\scripts\vectorize_image.py' '<input.png>' --out-dir '<output-dir>' --base-name '<name>' --mode both
```

If OpenCV is unavailable, `--mode pixel` still works with Pillow alone. For `--mode trace`, install or make available `opencv-python-headless` only with the user's approval when network or out-of-workspace writes are required.

## Output Quality Rules

- For exact requests, never rely only on manual SVG recreation or text/font matching. Fonts and antialiasing will drift.
- For logos generated as PNGs, prefer the pixel-perfect SVG as the primary answer when the user says "completely identical".
- For design handoff, also include a traced SVG when OpenCV is available.
- Do not claim the traced file is 100% identical. Reserve that claim for the pixel-exact file at native size.
- Keep original raster files unchanged.

## Script Notes

The script supports:

- `--mode pixel`: group same-color horizontal pixel runs into SVG path rectangles.
- `--mode trace`: threshold colored/non-white foreground pixels, extract contours, and write editable SVG paths.
- `--mode both`: create both outputs.
- `--threshold`: tune trace foreground detection; lower values include fainter antialiased pixels.
