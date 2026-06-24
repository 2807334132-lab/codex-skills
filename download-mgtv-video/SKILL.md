---
name: download-mgtv-video
description: Download public MangoTV/MGTV video pages from m.mgtv.com or www.mgtv.com into local standard MP4 files. Use when the user gives an MGTV link and asks to save, download, archive, convert, or make the video playable locally, especially when HLS fragments need to be merged or remuxed.
---

# Download MGTV Video

## Workflow

Use `scripts/download_mgtv_video.py` for the normal path. It wraps the working process:

1. Ensure `yt-dlp` is available.
2. Ensure an ffmpeg binary is available through `imageio-ffmpeg`.
3. Ask `yt-dlp` to download the best available MGTV format.
4. Inspect the result. If the file is an MPEG-TS/HLS stream with an `.mp4` extension, remux it to a standard MP4 and keep the raw stream as `.raw.ts`.
5. Report the final file path, resolution/metadata when available, and any backup raw file.

Run from the target output folder unless the user requested another location:

```powershell
& "<python>" "<skill-dir>\scripts\download_mgtv_video.py" "<mgtv-url>" --output-dir "<folder>"
```

Use the bundled Codex Python when system Python is not on PATH. In Codex desktop, `load_workspace_dependencies` can reveal that path.

## Options

- `--format FORMAT`: pass a yt-dlp format selector. Default is `best`. For 720p, use the numeric format id after checking formats or use `best[height<=720]/best`.
- `--name NAME`: set a clean base filename without extension.
- `--keep-raw`: keep the raw HLS/MPEG-TS stream even after successful remux.

To inspect available formats before downloading:

```powershell
& "<python>" -m yt_dlp -F "<mgtv-url>"
```

## Completion Checks

After downloading, verify:

- The final file exists and has non-trivial size.
- The first bytes contain `ftyp`, which indicates a standard MP4 container.
- If ffmpeg reports corrupt packets at HLS segment boundaries but still completes, treat the remux as acceptable when it produces the full-duration MP4.

Tell the user the absolute path to the final MP4. If a raw backup was kept or created, mention that separately.
