---
name: minimal-wallpaper
description: Generate refined minimalist desktop wallpapers and optionally set them as the Windows desktop background. Use when Codex is asked to create a high-end, premium, elegant, minimalist, modern, abstract, or designer desktop wallpaper; crop or resize a generated wallpaper to the current screen; save wallpaper files; or change the desktop background.
---

# Minimal Wallpaper

## Overview

Use this skill to create tasteful desktop wallpapers with restrained composition, generous negative space, and screen-correct sizing. Prefer the built-in image generation path for the artwork, then use the bundled script to crop, save, and optionally set the wallpaper.

## Workflow

1. Get the primary screen size before generating or processing:

```powershell
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::PrimaryScreen.Bounds
```

2. Generate one image with the `imagegen` skill or built-in image generation tool. Ask for a wallpaper-safe composition:
   - no text, logos, people, or recognisable brands;
   - calm negative space for desktop icons;
   - focal interest away from the icon-heavy left edge unless the user requests otherwise;
   - restrained colors and subtle texture instead of busy detail.

3. Inspect the generated image. Reject outputs that are too busy, contain text/watermarks, or feel like a generic gradient.

4. Run `scripts/prepare_wallpaper.py` to crop and resize the selected image to the screen:

```powershell
python scripts/prepare_wallpaper.py --input "C:\path\generated.png" --output "C:\Users\<user>\Pictures\Codex Wallpapers\wallpaper.png" --width 1463 --height 914 --set
```

5. Show or report the final saved path. If `--set` was used, confirm that the Windows wallpaper registry points to the final file.

## Prompt Pattern

Use this as a starting point and adapt to the user's taste:

```text
Use case: stylized-concept
Asset type: Windows desktop wallpaper for a <width>x<height> screen
Primary request: Create an elegant minimalist designer wallpaper with premium visual taste.
Scene/backdrop: abstract full-screen composition, soft warm off-white and graphite gray base, subtle brushed paper texture, faint architectural geometry, one thin muted sage line and a small deep charcoal accent for balance.
Subject: no characters, no objects, no text, no logos; pure refined abstract design.
Composition: wide desktop wallpaper, calm negative space for icons, focal interest slightly right of center, clean margins, no busy detail.
Style: high-end editorial minimalism, sophisticated, modern interior-design mood, subtle depth, soft natural light, matte finish, restrained color palette, crisp but not harsh.
Avoid: text, watermark, brand marks, clutter, neon colors, generic gradients, cartoon style, photographic objects, people.
```

## Style Guidance

Good directions:

- warm off-white, graphite, soft stone, muted sage, silver gray, deep charcoal;
- architectural geometry, paper grain, matte surfaces, subtle shadow, layered planes;
- quiet editorial design, modern interior mood, museum-like composition.

Avoid directions:

- neon, saturated purple/blue gradients, flashy 3D blobs, obvious stock-photo scenery;
- center-heavy compositions that compete with icons;
- text or symbols that can look like branding.

## Notes

- Do not overwrite an existing wallpaper unless the user explicitly asks.
- Copy generated images into a stable wallpaper folder such as `Pictures\Codex Wallpapers`; do not set a wallpaper directly from a temporary location.
- Keep the original generated image in place when copying it.
- If the user asks for a different mood, preserve the minimalist constraints and adjust palette/materials instead of adding clutter.
