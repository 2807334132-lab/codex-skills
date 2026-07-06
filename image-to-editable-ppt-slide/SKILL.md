---
name: image-to-editable-ppt-slide
description: Rebuild a provided reference image, screenshot, poster, infographic, or slide mockup into a one-slide editable PowerPoint deck. Use when the user asks to "拆解图片", "图片转PPT", "重建成PPT", "做成一页PPT", "editable PPT", or wants visual elements from an image recreated as separate PowerPoint objects while preserving the original layout and style.
---

# Image To Editable PPT Slide

## Purpose

Turn one visual reference image into a single PowerPoint slide whose major elements can be edited independently: text, headings, badges, cards, dividers, simple icons, shapes, and decorative backgrounds. Use raster fragments only for photographic or highly complex visual areas that cannot reasonably be recreated as native objects.

## Required Companion Skill

Use the `presentations:Presentations` skill for all PPTX generation and verification. Follow its requirements:

- Read its `SKILL.md` and required artifact-tool docs before authoring.
- Use `@oai/artifact-tool` from JavaScript ES modules.
- Do not use `python-pptx`.
- Render the finished deck and inspect the preview before delivery.
- Run overflow/layout checks where available.

## Workflow

1. Inspect the reference image.
   - Use visual inspection to identify canvas ratio, hierarchy, text, colors, repeated components, image areas, decorative shapes, spacing, and page chrome.
   - If the image contains readable text, transcribe it manually from the visual or use OCR only as a helper; proofread visible copy against the source.

2. Decide the decomposition boundary.
   - Recreate as editable PowerPoint objects: all visible text, number chips, simple icons, lines, pills, cards, dividers, geometric decorations, and simple vector marks.
   - Preserve as raster image layers: photos, paintings, complex textures, screenshots-with-many-small-pixels, highly detailed illustrations, and irregular image masks.
   - Do not place the entire source image as the final slide background unless the user explicitly wants a non-editable replica.

3. Build the slide at 16:9 unless the source image clearly uses another ratio.
   - Prefer `1280 x 720` slide size for new decks.
   - Scale coordinates from the source image proportionally.
   - Name important objects clearly, such as `main-title`, `chapter-pill`, `number-chip-01`, `right-content-card`, or `photo-fragment`.

4. Recreate the visual system.
   - Match the source palette, type scale, alignment, spacing, shadows, rounded corners, and page markers.
   - Use native text boxes for all text.
   - Use native shapes for simple icons where practical so the result remains editable.
   - Use embedded image assets for cropped photographic fragments.
   - Keep decorative shapes inside the slide canvas unless an intentional bleed is required and the verification tool accepts it.

5. Export and verify.
   - Export the `.pptx` to the user's requested path or to an `outputs/` folder.
   - Render a PNG preview of the final PPTX, not only the in-memory slide.
   - Inspect visually for text wrapping, clipped text, missing icons, unexpected strokes, image artifacts, and wrong layering.
   - Run the presentation overflow/layout test. If it fails, fix unintentional off-canvas objects and rerun.

6. Deliver concisely.
   - Return the final PPTX path.
   - Mention that the slide was rebuilt with editable elements and identify any raster fragments retained.
   - Cite the final PPTX slide when the host supports file citations.

## Practical Heuristics

- If SVG image insertion renders unreliably, rebuild icons from native PPT lines, rectangles, ellipses, and custom paths.
- If a decorative background shape causes overflow warnings, pull it inside the canvas or replace it with an in-canvas equivalent.
- If a cropped photo fragment carries unwanted borders from the source image, trim a few pixels and rerender.
- If Chinese text wraps unexpectedly, widen the text box before reducing font size.
- Keep the output to one slide unless the user asks for multiple pages.

## Example Request

User: "把这个图片的元素拆解出来，做成一页PPT"

Expected action: create a one-slide `.pptx` that visually follows the image, with editable text, badges, simple icons, cards, rules, and decorations; retain only photo-like regions as separate embedded image layers.
