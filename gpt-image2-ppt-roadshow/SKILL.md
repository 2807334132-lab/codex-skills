---
name: gpt-image2-ppt-roadshow
description: Create polished investor, roadshow, pitch, or business PowerPoint decks from source documents or notes using GPT-image2-style generated visuals, editable slide composition, table-of-contents and chapter divider structure, image-rich business design, and rendered layout QA. Use when the user asks to turn a DOCX/PDF/Markdown/topic into a high-design PPT, roadshow deck, investment presentation, investor reading deck, visually rich slides, or says the existing PPT is ugly/plain and wants images, business visual design, GPT-image, GPT-image2, or ppt-master redesign.
---

# GPT-image2 PPT Roadshow

## Operating Rule

Produce a finished PPTX, not just a plan. Keep slide text editable whenever possible, and use generated images as visual assets, backgrounds, chapter dividers, or focal panels rather than baking all text into bitmaps. For investor/business decks, default to a structured, image-rich reading deck with a cover, table of contents, chapter dividers, and rendered visual QA.

## Default Deck Structure

Use 12-16 slides by default for a source-document roadshow deck unless the user specifies a count. Prefer this rhythm:

1. Cover: big thesis, source theme, strong hero image.
2. Table of contents: 3-4 chapters with concise investor logic.
3. Chapter divider 01: trend, context, or market shift.
4. Evidence or framing slide: what is changing and why it matters.
5. Opportunity slide: 3-4 drivers or curves.
6. Operating model slide: workflow, capability stack, or value chain.
7. Chapter divider 02: product, assets, business model, or execution.
8. System or model slide: from idea to repeatable engine.
9. Asset/evidence slide: IP, process, data, customers, channels, or defensibility.
10. Chapter divider 03: risks, constraints, or path to scale.
11. Risk slide: red lines, mitigations, decision constraints.
12. Breakthrough/strategy slide: how the model scales beyond the obvious limits.
13. Roadmap slide: 3 phases, milestones, or investment use of proceeds.
14. Closing slide: future state, core thesis, memorable final statement.

Adjust the chapter names to the source. Good investor chapter arcs include:

- Trend & Opportunity / Model & Assets / Risk & Scaling
- Problem & Timing / Solution & Moat / Execution & Ask
- Market Shift / Product Engine / Growth Path

## Workflow

1. Ingest the source.
   - Read DOCX/PDF/Markdown/text into a clean markdown or outline source.
   - Preserve source-only claims. If market, finance, legal, or current facts are needed and not in the source, verify them before using.
   - Create a short source ledger: source path, extraction method, and any caveats.

2. Shape the investor narrative.
   - Identify audience, purpose, desired tone, and expected use: live pitch, investor reading deck, internal roadshow, or public presentation.
   - Use conclusion-first logic: thesis, tension, opportunity, operating model, assets/moat, risk, roadmap, close.
   - Split dense source sections across chaptered slides instead of compressing them into a document-like deck.
   - Write one main message per slide. Use compact bullets, short labels, and clear evidence blocks.

3. Define visual direction before building.
   - Choose a restrained business palette with contrast and one or two accent colors.
   - Set slide rhythm: full-bleed image cover, table of contents, atmospheric chapter dividers, structured framework slides, dense evidence slides, and closing vision.
   - Avoid repetitive white cards, decorative gradients, placeholder art, tiny text, and one-hue palettes.
   - Use image masks, split panels, dark overlays, edge bands, and generous whitespace to make images feel designed rather than pasted in.

4. Generate image assets.
   - Use GPT-image2 or the available image generation tool for custom bitmap assets when the deck needs richer design.
   - Prompt for concept images without text, logos, watermarks, numerals, charts, or UI labels.
   - Generate enough assets to create variety. For a 12-16 slide investor deck, usually create 6-8 images:
     - cover hero;
     - chapter divider 01 visual;
     - opportunity or market shift visual;
     - operating model or workflow visual;
     - asset/moat or business engine visual;
     - risk/constraint visual;
     - ecosystem/scaling visual;
     - closing vision.
   - Copy generated assets into the project workspace, for example `work/presentations/<slug>/assets_gpt2/`, so the final PPTX does not depend on transient generation folders.

5. Build the PPTX.
   - Use the presentation tooling available in the environment; prefer editable PowerPoint text, shapes, tables, and charts.
   - Use generated images as full-bleed backgrounds, chapter divider artwork, split image panels, masked visual anchors, or quiet texture bands.
   - Include a real table of contents slide for investor reading decks unless the user explicitly asks for a very short deck.
   - Include chapter divider slides when the deck has 10+ slides or 3+ narrative sections.
   - Keep title hierarchy clear: one main message per slide, compact supporting copy, and investor-readable evidence blocks.
   - Put final deck outputs under `outputs/` with a clear name such as `<slug>_gptimage2.pptx` or `<slug>_gptimage2_enhanced.pptx`.

6. Render and inspect.
   - Render every slide to PNG.
   - Create a contact sheet for quick visual review.
   - Inspect slide dimensions, slide count, media count, missing assets, text overflow, overlap, contrast, and whether each image is visible and relevant.
   - Check that the table of contents and chapter dividers are present when expected.
   - Check that text remains editable PPT objects and that images are embedded in the PPTX.
   - If browser preview is available, open the local preview. If local file/data/localhost preview is blocked, state that and rely on rendered PNG/contact-sheet QA.

7. Iterate on design.
   - If slides feel plain, add a stronger visual anchor, change crop/mask treatment, or introduce a chapter divider before adding more words.
   - If slides feel cluttered, reduce copy, increase whitespace, and split dense material into framework plus evidence.
   - If an image competes with text, crop/dim/mask it or move it to a separate visual zone.
   - If visual rhythm is repetitive, alternate full-bleed image slides, split-panel slides, framework diagrams, and compact evidence pages.

8. Deliver.
   - Provide the final PPTX path, preview/contact-sheet path, and a brief QA note.
   - Mention slide count, whether images are embedded, and whether editable text was preserved.
   - Mention any unverified source claims or limitations.

## GPT-image Prompt Patterns

Use concise prompts that describe mood, composition, and business relevance. Avoid asking the model to draw readable text.

Opening hero:
`Editorial cinematic image for an investor presentation about <theme>, premium business visual, <core metaphor>, generous negative space, warm light, realistic but slightly art-directed, no text, no logo, no watermark.`

Chapter divider:
`Premium business editorial image for a chapter divider about <chapter theme>, symbolic but concrete visual metaphor, strong negative space for overlay title, sophisticated lighting, no text, no logo, no watermark.`

Opportunity or market shift:
`Premium editorial image visualizing <market shift or opportunity>, modern business environment, layered composition, confident and analytical mood, no text, no logo, no watermark.`

Operating model:
`High-end business concept image showing <workflow, AI operations, product system, or value chain>, human decision-maker plus digital systems, clean modern workspace, no readable text, no logo, no watermark.`

Risk or constraint:
`Sophisticated business image showing <risk, compliance boundary, bottleneck, or pressure>, controlled contrast, serious but not alarming, abstract-realistic composition, no text, no logo, no watermark.`

Closing vision:
`Cinematic optimistic image for closing slide, <future state>, path forward, elegant business atmosphere, clean negative space for title overlay, no text, no logo, no watermark.`

## Design Checklist

Before final response, verify:

- PPTX opens/export succeeds.
- Slide count fits the requested scope; default investor reading deck is usually 12-16 slides.
- Cover, table of contents, chapter dividers, body slides, roadmap, and closing slide are present when appropriate.
- All generated images are embedded or available in the workspace.
- The deck uses multiple image roles: hero, divider, focal panel, supporting visual, and closing image.
- Every slide has one clear message.
- Text is readable on 16:9 slides and does not overlap images or page edges.
- Visual style is business-polished, premium, and varied, not a document pasted into slides.
- The preview contact sheet shows varied slide rhythm and no obvious clipping.
- Final answer gives exact local paths.
