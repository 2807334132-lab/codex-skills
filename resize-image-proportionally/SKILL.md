---
name: resize-image-proportionally
description: Resize raster images while preserving aspect ratio. Use when the user asks to change an image to a target pixel length, long edge, width, or height, especially for PNG/JPG/JPEG/BMP/GIF assets where the original image should be preserved and the output dimensions should be verified.
---

# Resize Image Proportionally

## Workflow

1. Confirm the source file path and inspect the original pixel dimensions before editing.
2. Interpret ambiguous Chinese image-size requests carefully:
   - The Chinese terms for "length", "long edge", or "longest edge" usually mean resize the long edge to the target pixel value.
   - The Chinese term for "width" means target width.
   - The Chinese term for "height" means target height.
   - If the requested meaning changes the output materially and cannot be inferred from context, ask one concise question.
3. Preserve the original file unless the user explicitly asks to overwrite it.
4. Write the resized image next to the source by default, using a suffix like `_950px`, `_790px`, or `_w950`.
5. Verify the output dimensions after saving and report the new file path plus final size.

## Script

Use `scripts/resize-image.ps1` for repeatable Windows image resizing:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\TANB\.codex\skills\resize-image-proportionally\scripts\resize-image.ps1" -InputPath "D:\path\image.png" -LongEdge 950
```

Useful modes:

```powershell
# Resize the longest edge to 950px.
-LongEdge 950

# Resize to a specific width and compute height proportionally.
-Width 950

# Resize to a specific height and compute width proportionally.
-Height 950

# Provide an explicit output path.
-OutputPath "D:\path\image_950px.png"

# Replace a previously generated output file with the same path.
-Overwrite
```

## Validation

After resizing, reopen the output image and check its dimensions. Trust the verified file dimensions over mental estimates because proportional resizing is rounded to whole pixels.

Examples:

- A landscape image originally `1125x844`, resized with `-LongEdge 950`, should produce `950x713`.
- A landscape image originally `1448x1086`, resized with `-LongEdge 790`, should produce `790x592`.

## Reporting

Tell the user:

- Whether the original file was preserved.
- The output file path.
- The verified dimensions in `WIDTH x HEIGHTpx`.
