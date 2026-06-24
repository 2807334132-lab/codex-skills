---
name: precise-infographic-raster-edit
description: Precisely edit raster infographic images while preserving non-target pixels. Use when the user asks to change a specific area of a screenshot, slide image, architecture diagram, chart, or business infographic, especially when generated image editing may accidentally alter surrounding text, icons, or layout. Supports local pixel-preserving redraws with Pillow after inspecting the image.
---

# Precise Infographic Raster Edit

## Workflow

1. Inspect the input image visually and identify the exact target region.
2. If the user wants a conceptual or stylistic transformation, a generated-image edit can be used for a draft.
3. If text, numbers, logos, or dense diagram content must stay unchanged, prefer deterministic local editing:
   - Load the original raster.
   - Clear or mask only the target region.
   - Redraw the requested shapes, labels, and separators.
   - Leave all other pixels untouched.
4. Use system fonts that support Chinese when needed, such as `msyhbd.ttc`, `msyh.ttc`, or `simhei.ttf`.
5. Save the result as a new sibling file. Do not overwrite the original unless the user explicitly asks.
6. Preview the output and iterate if text is cramped, misaligned, or visually weaker than the source.

## Validation

Check that:

- The requested region changed.
- Non-target text and icons are preserved.
- All labels are legible.
- The visual style matches the original color, stroke weight, spacing, and business presentation tone.

## Reporting

Give the saved absolute path and mention whether the final was a precise pixel-preserving edit or a generated-image draft.
