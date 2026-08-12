import argparse
import shutil
import subprocess
from pathlib import Path


def find_ffmpeg(explicit=None):
    if explicit:
        p = Path(explicit)
        if p.is_file():
            return str(p)
        raise FileNotFoundError(f"ffmpeg not found: {p}")
    found = shutil.which("ffmpeg")
    if found:
        return found
    candidates = [
        Path(r"C:\Program Files\Adobe\Adobe After Effects 2022\Support Files\Scripts\ScriptUI Panels\ffmpeg.exe"),
        Path(r"C:\Program Files\Adobe\Adobe After Effects 2022\Support Files\Scripts\ScriptUI Panels\(ffmpeg)\ffmpeg.exe"),
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError("ffmpeg was not found on PATH or in known Adobe locations")


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description="Extract transcription audio and optional subtitle-band frames")
    ap.add_argument("input", type=Path)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--ffmpeg")
    ap.add_argument("--subtitle-frames", action="store_true")
    ap.add_argument("--frame-interval", type=float, default=4.0)
    ap.add_argument("--bottom-fraction", type=float, default=0.18)
    args = ap.parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(args.input)
    if not 0.08 <= args.bottom_fraction <= 0.40:
        raise ValueError("--bottom-fraction must be between 0.08 and 0.40")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg(args.ffmpeg)
    wav = args.output_dir / "audio-16k-mono.wav"
    run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(args.input),
         "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)])
    if args.subtitle_frames:
        frames = args.output_dir / "subtitle-frames"
        frames.mkdir(exist_ok=True)
        fps = 1.0 / args.frame_interval
        top = 1.0 - args.bottom_fraction
        vf = f"fps={fps:.8f},scale=1280:-2,crop=iw:ih*{args.bottom_fraction:.6f}:0:ih*{top:.6f}"
        run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(args.input),
             "-vf", vf, "-q:v", "2", str(frames / "subtitle_%06d.jpg")])
    print(wav.resolve())


if __name__ == "__main__":
    main()

