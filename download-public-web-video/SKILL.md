---
name: download-public-web-video
description: Download publicly accessible web videos to the user's local workspace. Use when the user provides a video page URL or asks to save/download a web video from sites supported by common extractors such as yt-dlp, including HLS/MP4 streams, while respecting login, payment, DRM, copyright, and access restrictions. Also use when validating the downloaded file's duration, resolution, audio, and playback integrity.
---

# Download Public Web Video

## Workflow

1. Confirm the request is for a video the user is allowed to access. Do not bypass login, payment, geographic restrictions, DRM, or site protections.
2. Work in the user's current folder unless they specify another destination.
3. Check for `yt-dlp`, Python, and `ffmpeg`.
4. If `yt-dlp` is unavailable but Python is available, install or update it with `python -m pip install --user -U yt-dlp`.
5. If `ffmpeg` is unavailable, prefer `imageio-ffmpeg` as a user-level helper:

```powershell
python -m pip install --user -U imageio-ffmpeg
$ff=(python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
```

6. Probe the URL before downloading:

```powershell
python -m yt_dlp --ffmpeg-location $ff --no-playlist --print "%(title)s`n%(duration_string)s`n%(ext)s`n%(webpage_url)s" "<url>"
```

7. Download the best available single video, using a safe filename:

```powershell
python -m yt_dlp --ffmpeg-location $ff --no-playlist --restrict-filenames --merge-output-format mp4 -o "%(title).120s-%(id)s.%(ext)s" "<url>"
```

8. Validate the result:

```powershell
Get-Item -LiteralPath "<downloaded-file>" | Select-Object FullName,Length,LastWriteTime
& $ff -hide_banner -i "<downloaded-file>" -f null -
```

## Reporting

Tell the user:

- The saved absolute path.
- The title if known.
- Duration, resolution, file size, and whether audio/video decoded successfully.
- Any limitations, such as metadata extraction warnings, inaccessible protected content, or missing tools.

## Notes

- Prefer non-technical wording for the user-facing updates.
- Keep retry attempts bounded. If extraction fails because the content requires authentication, payment, or DRM removal, stop and explain the limitation.
- Do not delete unrelated files in the destination folder.
