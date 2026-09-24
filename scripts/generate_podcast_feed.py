#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_podcast_feed.py — Build a per-channel podcast RSS feed (docs/{channel}/feed.xml)
from audio_manifest.json + data/.video_metadata.json, so the channel can be subscribed to
in a real podcast app (Apple Podcasts, Overcast, ...) via "Add by URL".

Only stems that already have a Release-asset audio URL in audio_manifest.json are included
— this repo does not backfill audio for older videos that were transcribed straight from
YouTube's own captions (see channel_fetch.py). Each item links its transcript via the
Podcasting 2.0 <podcast:transcript> tag, pointing straight at the existing _FIN.srt/_GT.srt
(no format conversion needed — the namespace accepts application/srt).

Usage:
    python scripts/generate_podcast_feed.py <channel> [--out docs/{channel}/feed.xml]
"""
from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "audio_manifest.json"
META_CACHE_PATH = REPO_ROOT / "data" / ".video_metadata.json"
PAGES_BASE = "https://zhongzheng782.github.io/YoutubeAudio.Fetch"
CDN_BASE = "https://cdn.jsdelivr.net/gh/ZhongZheng782/YoutubeAudio.Fetch@main"

TAIPEI = timezone(timedelta(hours=8))


def load_episodes(channel: str) -> list[dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    meta_cache = json.loads(META_CACHE_PATH.read_text(encoding="utf-8")) if META_CACHE_PATH.exists() else {}

    episodes = []
    for stem, audio_url in manifest.items():
        if not stem.startswith(f"{channel}_"):
            continue
        video_id = stem[len(channel) + 1:]
        meta = meta_cache.get(video_id, {})
        title = meta.get("title") or stem
        date_str = meta.get("date") or ""
        try:
            pub_dt = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=8, tzinfo=TAIPEI)
        except ValueError:
            pub_dt = datetime.now(tz=TAIPEI)

        srt_path = None
        for suffix in ("_FIN.srt", "_GT.srt"):
            candidate = REPO_ROOT / "data" / channel / f"{stem}{suffix}"
            if candidate.exists():
                srt_path = f"data/{channel}/{stem}{suffix}"
                break

        episodes.append({
            "stem": stem,
            "video_id": video_id,
            "title": title,
            "pub_dt": pub_dt,
            "audio_url": audio_url,
            "srt_path": srt_path,
            "channel_name": meta.get("channel_name") or channel,
        })

    episodes.sort(key=lambda e: e["pub_dt"], reverse=True)
    return episodes


def placeholder_image_url(channel: str, episodes: list[dict]) -> str | None:
    keyframes_dir = REPO_ROOT / "data" / channel
    for ep in episodes:
        md_path = keyframes_dir / f"{ep['stem']}_keyframes.md"
        if md_path.exists():
            jpgs = sorted((keyframes_dir / f"{ep['stem']}_keyframes").glob("*.jpg"))
            if jpgs:
                rel = jpgs[0].relative_to(REPO_ROOT).as_posix()
                return f"{CDN_BASE}/{rel}"
    return None


def enclosure_length(audio_url: str) -> str:
    """Real byte size via a HEAD request — podcast apps use this to show download
    size/progress before playback starts. Best-effort: 0 is a valid (if unhelpful)
    fallback per the RSS spec, so a lookup hiccup shouldn't block feed generation."""
    req = urllib.request.Request(audio_url, method="HEAD", headers={"User-Agent": "curl/8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.headers.get("Content-Length", "0")
    except Exception:
        return "0"


def render_feed(channel: str, episodes: list[dict]) -> str:
    channel_name = episodes[0]["channel_name"] if episodes else channel
    channel_link = f"{PAGES_BASE}/"
    feed_self_url = f"{PAGES_BASE}/{channel}/feed.xml"
    image_url = placeholder_image_url(channel, episodes) or ""

    items = []
    for ep in episodes:
        transcript_tag = ""
        if ep["srt_path"]:
            transcript_url = f"{CDN_BASE}/{ep['srt_path']}"
            transcript_tag = (
                f'      <podcast:transcript url="{escape(transcript_url)}" '
                f'type="application/srt" language="zh"/>\n'
            )
        items.append(
            "    <item>\n"
            f"      <title>{escape(ep['title'])}</title>\n"
            f"      <guid isPermaLink=\"false\">{escape(ep['stem'])}</guid>\n"
            f"      <pubDate>{format_datetime(ep['pub_dt'])}</pubDate>\n"
            f"      <link>https://www.youtube.com/watch?v={escape(ep['video_id'])}</link>\n"
            f"      <description>{escape(ep['title'])}</description>\n"
            f"      <enclosure url=\"{escape(ep['audio_url'])}\" type=\"audio/mp4\" "
            f"length=\"{enclosure_length(ep['audio_url'])}\"/>\n"
            f"{transcript_tag}"
            "    </item>\n"
        )

    image_block = (
        f'    <itunes:image href="{escape(image_url)}"/>\n'
        f"    <image>\n"
        f"      <url>{escape(image_url)}</url>\n"
        f"      <title>{escape(channel_name)}</title>\n"
        f"      <link>{escape(channel_link)}</link>\n"
        f"    </image>\n"
    ) if image_url else ""

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" '
        'xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
        'xmlns:podcast="https://podcastindex.org/namespace/1.0" '
        'xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{escape(channel_name)}</title>\n"
        f"    <link>{escape(channel_link)}</link>\n"
        f'    <atom:link href="{escape(feed_self_url)}" rel="self" type="application/rss+xml"/>\n'
        "    <language>zh-tw</language>\n"
        f"    <itunes:author>{escape(channel_name)}</itunes:author>\n"
        "    <itunes:explicit>false</itunes:explicit>\n"
        '    <itunes:category text="Business"><itunes:category text="Investing"/></itunes:category>\n'
        f"    <description>{escape(channel_name)} — 由 YoutubeAudio.Fetch 自動彙整自 YouTube 頻道音訊</description>\n"
        f"{image_block}"
        + "".join(items) +
        "  </channel>\n"
        "</rss>\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("channel")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    episodes = load_episodes(args.channel)
    out_path = Path(args.out) if args.out else REPO_ROOT / "docs" / args.channel / "feed.xml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_feed(args.channel, episodes), encoding="utf-8")
    print(f"[generate_podcast_feed] {args.channel}: {len(episodes)} episode(s) -> {out_path}")
