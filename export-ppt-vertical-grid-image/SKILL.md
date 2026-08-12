---
name: export-ppt-vertical-grid-image
description: Export a local PowerPoint deck into a high-resolution vertical overview image with the cover across the top and selected slides arranged in a grid below. Use when the user asks to turn a PPT/PPTX into a 3:4 portrait image, 九宫格/宫格长图, slide overview poster, cover-plus-thumbnails image, or a layout matching a supplied PPT contact-sheet reference.
---

# Export PPT Vertical Grid Image

Create a deterministic raster composition from the actual slide renders. Preserve slide text and artwork exactly; do not regenerate slides with an image model.

## Workflow

1. Inspect the reference image and the full deck. Confirm the requested canvas ratio, grid rows/columns, and slide order.
2. Render every slide to PNG. On Windows with Microsoft PowerPoint, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/export_ppt_slides.ps1 `
  -InputPptx "<input.pptx>" -OutputDir "<work/slides>"
```

3. Select pages deliberately:
   - Put slide 1 across the top unless the user names another cover.
   - For an explicitly ordered grid, follow that order.
   - If only “3×3 below the cover” is requested, default to slides 2–10 in reading order.
   - If the user asks for a summary rather than sequential pages, remove pure divider/repetition slides and select the strongest content pages.
4. Compose the final image with `scripts/build_vertical_grid.py`:

```powershell
python scripts/build_vertical_grid.py `
  --slides-dir "<work/slides>" `
  --output "<outputs/overview.jpg>" `
  --ratio 3:4 --width 1800 `
  --cover 1 --grid-start 2 --rows 3 --cols 3 `
  --closing-slide 15 `
  --main-text "<closing claim>" `
  --sub-text "<short closing line>"
```

5. Open the final image at full resolution and inspect the cover, every thumbnail, gutters, and closing banner.

## Layout Rules

- Keep the cover and grid slides at their original aspect ratio. Never stretch or crop their content.
- Use narrow, even gutters similar to the supplied reference.
- A full-width 16:9 cover plus a 3×3 grid does not naturally fill a 3:4 canvas. Use the remaining height as a restrained closing banner derived from the last slide. This preserves all slide content while meeting the exact ratio.
- Prefer 1800×2400 or larger for a 3:4 deliverable. Save JPEG at quality 95 with 4:4:4 chroma, or PNG when lossless output is requested.
- Keep intermediate renders under the task work directory. Put only final user-facing images in the designated outputs directory.

## Validation

- Confirm `width / height` equals the requested ratio exactly.
- Confirm the cover is first and the grid has exactly `rows × columns` slides.
- Verify page order against the source deck.
- Check that no title, footer, person, chart, or edge content is clipped.
- Check small text remains readable when viewed at 100%.
- Reject visible stretching, unintended blank bands, clipped banner text, uneven gutters, or low-resolution slide renders.

## Reporting

Return the final image only, state its pixel dimensions and arrangement, and show an inline preview when the client supports local-image rendering.
