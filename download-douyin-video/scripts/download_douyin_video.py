#!/usr/bin/env python3
"""Download a public Douyin video from a share URL."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)


def request(url: str, *, referer: str | None = None) -> urllib.request.addinfourl:
    headers = {"User-Agent": UA}
    if referer:
        headers["Referer"] = referer
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30)


def read_text(url: str, *, referer: str | None = None) -> tuple[str, str]:
    with request(url, referer=referer) as response:
        data = response.read()
        final_url = response.geturl()
    return data.decode("utf-8", errors="replace"), final_url


def extract_url(text: str) -> str:
    match = re.search(r"https?://[^\s]+", text)
    if not match:
        raise ValueError("No URL found in input.")
    return match.group(0).rstrip(".,;:，。；：")


def extract_video_id(url: str) -> str | None:
    patterns = [
        r"/video/(\d+)",
        r"/share/video/(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def share_url_from(url: str) -> str:
    _, final_url = read_text(url)
    video_id = extract_video_id(final_url) or extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not determine Douyin video ID from {final_url}")
    return f"https://www.iesdouyin.com/share/video/{video_id}/"


def extract_router_data(page: str) -> dict:
    match = re.search(r"<script>window\._ROUTER_DATA\s*=\s*(\{.*?\})</script>", page, re.S)
    if not match:
        raise ValueError("Could not find window._ROUTER_DATA in the share page.")
    return json.loads(html.unescape(match.group(1)))


def find_play_url(router_data: dict) -> str:
    loader = router_data.get("loaderData", {})
    for value in loader.values():
        if not isinstance(value, dict):
            continue
        info = value.get("videoInfoRes")
        if not isinstance(info, dict):
            continue
        items = info.get("item_list") or []
        for item in items:
            video = item.get("video") or {}
            play_addr = video.get("play_addr") or {}
            urls = play_addr.get("url_list") or []
            if urls:
                return urls[0]
    raise ValueError("No public play_addr URL found in router data.")


def download(url: str, output: Path, referer: str) -> None:
    with request(url, referer=referer) as response:
        data = response.read()
    if len(data) < 1024:
        raise ValueError("Downloaded response is too small to be a video.")
    output.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Douyin share text or URL")
    parser.add_argument("--output", "-o", default="douyin_video.mp4", help="Output MP4 path")
    args = parser.parse_args()

    try:
        url = extract_url(args.input)
        share_url = share_url_from(url)
        page, _ = read_text(share_url, referer="https://v.douyin.com/")
        play_url = find_play_url(extract_router_data(page))
        output = Path(args.output)
        download(play_url, output, referer=share_url)
        print(output.resolve())
        return 0
    except (OSError, ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
