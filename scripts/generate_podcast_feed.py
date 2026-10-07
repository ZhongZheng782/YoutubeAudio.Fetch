#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_podcast_feed.py — Build a per-channel podcast RSS feed (docs/{channel}/feed.xml)
from audio_manifest.json + data/.video_metadata.json, so the channel can be subscribed to
in a real podcast app (Apple Podcasts, Overcast, ...) via "Add by URL".

Only stems that already have a Release-asset audio URL in audio_manifest.json are included
— this repo does not backfill audio for older videos that were transcribed straight from
YouTube's own captions (see channel_fetch.py). Each item links its transcript via the
Podcasting 2.0 <podcast:transcript> tag. As of March 2026 Apple Podcasts only accepts VTT
(it dropped SRT support), so each _FIN.srt/_GT.srt is converted to WebVTT and published to
docs/{channel}/transcripts/{stem}.vtt for GitHub Pages to serve with the right content type.

Usage:
    python scripts/generate_podcast_feed.py <channel> [--out docs/{channel}/feed.xml]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from urllib.parse import quote
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_readme_index import fetch_video_meta  # noqa: E402 — shares the yt-dlp lookup + cache format

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "audio_manifest.json"
META_CACHE_PATH = REPO_ROOT / "data" / ".video_metadata.json"
PAGES_BASE = "https://zhongzheng782.github.io/YoutubeAudio.Fetch"
CDN_BASE = "https://cdn.jsdelivr.net/gh/ZhongZheng782/YoutubeAudio.Fetch@main"
# GitHub Release assets are always served as application/octet-stream with a
# forced download disposition, regardless of what's declared at upload time —
# podcast apps (Apple Podcasts confirmed) refuse to play that. This Worker
# (cloudflare-worker/) proxies the same Release bytes with corrected headers.
WORKER_BASE = "https://youtubeaudio.wenchiehlee1020.workers.dev"

TAIPEI = timezone(timedelta(hours=8))
# This repo's *.srt is not actually SRT despite the extension — it's a custom pseudo-SRT
# (see channel_fetch.py's transcript_to_pseudo_srt / _pseudo_srt_timestamp): a metadata
# header followed by "(MM:SS.mmm) text" lines, one timestamp per cue (no end time, no
# sequence numbers). MM is unbounded total minutes, not clock-wrapped hours:minutes.
PSEUDO_SRT_CUE_RE = re.compile(r"^\((\d+):(\d{2}\.\d{3})\)\s?(.*)$")
DEFAULT_CUE_DURATION = 4.0


def _format_vtt_timestamp(total_seconds: float) -> str:
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"


def parse_pseudo_srt_cues(pseudo_srt_text: str) -> list[tuple[float, str]]:
    cues = []
    for line in pseudo_srt_text.replace("\r\n", "\n").split("\n"):
        match = PSEUDO_SRT_CUE_RE.match(line.strip())
        if not match:
            continue
        minutes, seconds, text = match.groups()
        start = int(minutes) * 60 + float(seconds)
        if text.strip():
            cues.append((start, text.strip()))
    return cues


def srt_to_vtt(pseudo_srt_text: str) -> str:
    cues = parse_pseudo_srt_cues(pseudo_srt_text)
    blocks = ["WEBVTT", ""]
    for i, (start, text) in enumerate(cues):
        end = cues[i + 1][0] if i + 1 < len(cues) else start + DEFAULT_CUE_DURATION
        if end <= start:
            end = start + 1.0
        blocks.append(f"{_format_vtt_timestamp(start)} --> {_format_vtt_timestamp(end)}")
        blocks.append(text)
        blocks.append("")
    return "\n".join(blocks).rstrip("\n") + "\n"


def load_episodes(channel: str) -> list[dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    meta_cache = json.loads(META_CACHE_PATH.read_text(encoding="utf-8")) if META_CACHE_PATH.exists() else {}
    cache_dirty = False

    episodes = []
    for stem, audio_url in manifest.items():
        if not stem.startswith(f"{channel}_"):
            continue
        video_id = stem[len(channel) + 1:]
        if video_id not in meta_cache:
            # Audio can land in the manifest before generate_readme_index.py ever looks
            # this video up (it only queries stems that already have a _keyframes.md,
            # i.e. already transcribed) — without this, a still-transcribing episode
            # shows its raw stem as the title and sorts as "published today" forever.
            fetched = fetch_video_meta(video_id)
            if fetched is not None:
                meta_cache[video_id] = fetched
                cache_dirty = True
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
            "channel": channel,
            "title": title,
            "pub_dt": pub_dt,
            "audio_url": audio_url,
            "srt_path": srt_path,
            "channel_name": meta.get("channel_name"),
        })

    if cache_dirty:
        META_CACHE_PATH.write_text(
            json.dumps(meta_cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    episodes.sort(key=lambda e: e["pub_dt"], reverse=True)
    return episodes


def all_channels() -> list[str]:
    """Every channel with at least one audio-backed episode in the manifest — video_id is
    a fixed 11 chars, so channel = stem[:-12] (strips "_" + the id) rather than splitting
    on "_", which would break on a channel slug containing an underscore."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return sorted({stem[:-12] for stem in manifest})


def load_all_episodes() -> list[dict]:
    """Every channel's episodes merged into one newest-first list, for the combined
    cross-channel feed (one subscription instead of one per channel)."""
    episodes = [ep for channel in all_channels() for ep in load_episodes(channel)]
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


def episode_image_url(ep: dict) -> str | None:
    """This specific episode's own first keyframe thumbnail, so a combined multi-channel
    feed gives listeners a per-episode visual cue of which channel it came from (on top
    of the title prefix) — distinct art per item is supported by Apple Podcasts, Overcast
    and Pocket Casts in the episode list, not just a static per-feed/per-channel image."""
    keyframes_dir = REPO_ROOT / "data" / ep["channel"] / f"{ep['stem']}_keyframes"
    jpgs = sorted(keyframes_dir.glob("*.jpg")) if keyframes_dir.exists() else []
    if not jpgs:
        return None
    rel = jpgs[0].relative_to(REPO_ROOT).as_posix()
    return f"{CDN_BASE}/{rel}"


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


def _timeline_label(seconds: float) -> str:
    total = int(seconds)
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def render_transcript_timeline(ep: dict) -> str:
    """Render a compact HTML timeline that remains visible in RSS descriptions."""
    if not ep["srt_path"]:
        return ""
    from html import escape as html_escape

    srt_text = (REPO_ROOT / ep["srt_path"]).read_text(encoding="utf-8")
    cues = parse_pseudo_srt_cues(srt_text)
    lines = []
    for start, cue_text in cues:
        page_url = (
            f"{PAGES_BASE}/?channel={quote(ep['channel'])}"
            f"&episode={quote(ep['stem'])}&t={int(start)}"
        )
        lines.append(
            f'<p><a href="{html_escape(page_url, quote=True)}">'
            f'[{_timeline_label(start)}]</a> {html_escape(cue_text)}</p>'
        )
    return "\n".join(lines)


def write_vtt_transcript(channel: str, ep: dict) -> str | None:
    """Convert ep's SRT to WebVTT and publish it under docs/, returning the Pages URL
    (or None if there's no transcript). Apple Podcasts stopped accepting SRT in March
    2026, so this is the only format podcast:transcript can point to and have it show."""
    if not ep["srt_path"]:
        return None
    srt_text = (REPO_ROOT / ep["srt_path"]).read_text(encoding="utf-8")
    vtt_dir = REPO_ROOT / "docs" / channel / "transcripts"
    vtt_dir.mkdir(parents=True, exist_ok=True)
    vtt_path = vtt_dir / f"{ep['stem']}.vtt"
    vtt_path.write_text(srt_to_vtt(srt_text), encoding="utf-8")
    return f"{PAGES_BASE}/{channel}/transcripts/{ep['stem']}.vtt"


def render_feed(channel: str, episodes: list[dict], *, combined: bool = False) -> str:
    """channel is the per-channel slug normally, or "all" for the combined cross-channel
    feed — combined=True adds a 【頻道名稱】 title prefix, an <itunes:author>, and a
    per-episode <itunes:image> to each item so a single subscription still lets listeners
    tell channels apart (see episode_image_url)."""
    channel_name = (
        "YoutubeAudio.Fetch 全頻道彙整" if combined
        else next((e["channel_name"] for e in episodes if e["channel_name"]), channel)
    )
    channel_link = f"{PAGES_BASE}/"
    feed_self_url = f"{PAGES_BASE}/feed.xml" if combined else f"{PAGES_BASE}/{channel}/feed.xml"
    image_url = placeholder_image_url(channel, episodes) or "" if not combined else (
        next((episode_image_url(e) for e in episodes if episode_image_url(e)), "")
    )

    items = []
    for ep in episodes:
        transcript_tag = ""
        transcript_url = write_vtt_transcript(ep["channel"], ep)
        if transcript_url:
            transcript_tag = (
                f'      <podcast:transcript url="{escape(transcript_url)}" '
                f'type="text/vtt" rel="captions" language="zh" lang="zh-TW"/>\n'
            )
        ep_title = f"【{ep['channel_name'] or ep['channel']}】{ep['title']}" if combined else ep["title"]
        extra_tags = ""
        if combined:
            ep_image_url = episode_image_url(ep)
            extra_tags += f"      <itunes:author>{escape(ep['channel_name'] or ep['channel'])}</itunes:author>\n"
            if ep_image_url:
                extra_tags += f'      <itunes:image href="{escape(ep_image_url)}"/>\n'
        items.append(
            "    <item>\n"
            f"      <title>{escape(ep_title)}</title>\n"
            f"      <guid isPermaLink=\"false\">{escape(ep['stem'])}</guid>\n"
            f"      <pubDate>{format_datetime(ep['pub_dt'])}</pubDate>\n"
            f"      <link>https://www.youtube.com/watch?v={escape(ep['video_id'])}</link>\n"
            f"      <description>{escape(ep_title)}</description>\n"
            f"      <content:encoded><![CDATA[{render_transcript_timeline(ep)}]]></content:encoded>\n"
            f"      <enclosure url=\"{escape(WORKER_BASE)}/audio/{escape(ep['stem'])}.m4a\" "
            f"type=\"audio/mp4\" length=\"{enclosure_length(ep['audio_url'])}\"/>\n"
            f"{extra_tags}"
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
        'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
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
        f"    <description>"
        + escape(
            "各財經 YouTube 頻道合輯，單一訂閱涵蓋所有頻道（每集標題以【頻道名稱】標示來源）"
            if combined else f"{channel_name} — 由 YoutubeAudio.Fetch 自動彙整自 YouTube 頻道音訊"
        )
        + "</description>\n"
        f"{image_block}"
        + "".join(items) +
        "  </channel>\n"
        "</rss>\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("channel", nargs="?", help="e.g. fubonsec")
    group.add_argument("--all", action="store_true", help="Combined feed across every channel (docs/feed.xml)")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    if not args.channel and not args.all:
        parser.error("either a channel or --all is required")

    if args.all:
        episodes = load_all_episodes()
        out_path = Path(args.out) if args.out else REPO_ROOT / "docs" / "feed.xml"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_feed("all", episodes, combined=True), encoding="utf-8")
        print(f"[generate_podcast_feed] all: {len(episodes)} episode(s) -> {out_path}")
    else:
        episodes = load_episodes(args.channel)
        out_path = Path(args.out) if args.out else REPO_ROOT / "docs" / args.channel / "feed.xml"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_feed(args.channel, episodes), encoding="utf-8")
        print(f"[generate_podcast_feed] {args.channel}: {len(episodes)} episode(s) -> {out_path}")
