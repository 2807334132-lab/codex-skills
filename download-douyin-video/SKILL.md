---
name: download-douyin-video
description: Download public Douyin videos from share text, short links, v.douyin.com URLs, douyin.com video URLs, or iesdouyin.com share pages. Use when the user asks Codex to save, download, archive, or extract a Douyin/TikTok China video to a local MP4 file.
---

# Download Douyin Video

## Overview

Use this workflow to download public Douyin videos from share links. Respect platform access limits and copyright: download only content the user is permitted to save, and do not attempt to bypass private content, login walls, paywalls, or DRM.

## Workflow

1. Extract the first Douyin URL from the user's message. Common inputs include copied Douyin share text with a `https://v.douyin.com/.../` short link.
2. Prefer `yt-dlp` first when available:

```powershell
python -m yt_dlp -o "douyin_video.%(ext)s" "<url>"
```

3. If `yt-dlp` reports that fresh cookies are needed, try browser cookies only when appropriate and without printing cookie values:

```powershell
python -m yt_dlp --cookies-from-browser chrome -o "douyin_video.%(ext)s" "<url>"
python -m yt_dlp --cookies-from-browser edge -o "douyin_video.%(ext)s" "<url>"
```

4. If `yt-dlp` cannot use cookies or Douyin blocks the web detail JSON, use the bundled helper script:

```powershell
python "<skill-dir>\scripts\download_douyin_video.py" "<url>" --output "douyin_video.mp4"
```

The helper resolves short links, fetches the mobile share page, extracts `window._ROUTER_DATA`, reads `video.play_addr.url_list[0]`, and saves the MP4.

## Notes

- If a short link resolves to `https://www.douyin.com/video/<id>`, the helper can derive `https://www.iesdouyin.com/share/video/<id>/`.
- Use an iPhone Safari user agent for the share page and `Referer: https://www.iesdouyin.com/share/video/<id>/` for the video request.
- If only a poster image is present and no `play_addr` exists, report that the page did not expose a downloadable public video URL.
- Confirm the result by checking that the file exists, has non-trivial size, and begins with an MP4 `ftyp` header when media tooling is unavailable.
