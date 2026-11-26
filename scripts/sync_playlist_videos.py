#!/usr/bin/env python3
"""Sync a `type: "playlist"` source's `videos` list in sources.json against the
live YouTube playlist.

`run_source_fetches.py` never looks at the real YouTube playlist — it only reads the
static `videos` array someone typed into sources.json. Saving a video to the playlist
on youtube.com does nothing on its own; this script is the "copy it over" step: it
lists the playlist's current videos via yt-dlp, finds the ones not yet in sources.json,
and adds them. Each new video's uploader channel gets a fresh entry in that playlist
source's `channel_policies` if one doesn't already exist, defaulting to
retention="selected" (fetch just that one curated video, no ongoing tracking) —
promoting a channel to "all"/"since_date" ongoing Daily tracking is a deliberate
decision left to a human editing sources.json, same as how `LEI｜The Market Memo` got
promoted out of the "selected" default.

Usage:
    python scripts/sync_playlist_videos.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/skill-youtube-channel-fetch/scripts"))
from channel_fetch import (  # type: ignore
    VIDEO_ID_RE,
    YT_DLP_JS_RUNTIME_ARGS,
    YT_DLP_LISTING_TIMEOUT,
    _run_yt_dlp,
    yt_dlp_cookie_args,
)


def list_playlist_live(playlist_url: str) -> list[dict]:
    """Current videos on the live YouTube playlist, newest-first, with uploader info."""
    args = ["yt-dlp", *YT_DLP_JS_RUNTIME_ARGS, *yt_dlp_cookie_args(), "--flat-playlist", "-J", playlist_url]
    proc = _run_yt_dlp(args, timeout=YT_DLP_LISTING_TIMEOUT)
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp playlist listing failed: {proc.stderr[:500]}")
    data = json.loads(proc.stdout)
    entries = []
    for e in data.get("entries", []):
        video_id = e.get("id", "")
        if not VIDEO_ID_RE.match(video_id):
            continue
        entries.append({
            "video_id": video_id,
            "title": e.get("title") or video_id,
            "channel_name": e.get("channel") or e.get("uploader") or "channel",
            "channel_id": e.get("channel_id") or "",
            "channel_url": e.get("channel_url") or e.get("uploader_url") or "",
        })
    return entries


def video_upload_date(video_id: str) -> str:
    """'YYYY-MM-DD' for a single video, '' if the lookup fails."""
    proc = _run_yt_dlp(
        ["yt-dlp", *YT_DLP_JS_RUNTIME_ARGS, *yt_dlp_cookie_args(), "--skip-download", "--print", "%(upload_date)s",
         f"https://www.youtube.com/watch?v={video_id}"],
        timeout=YT_DLP_LISTING_TIMEOUT,
    )
    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    if len(line) == 8 and line.isdigit():
        return f"{line[0:4]}-{line[4:6]}-{line[6:8]}"
    return ""


def sync_source(source: dict) -> dict[str, int]:
    existing_ids = {v["video_id"] for v in source.get("videos", [])}
    policies_by_url = {p.get("channel_url"): p for p in source.get("channel_policies", [])}
    live = list_playlist_live(source["url"])

    added_videos = added_channels = updated_selected = 0
    for entry in live:
        if entry["video_id"] in existing_ids:
            continue
        date = video_upload_date(entry["video_id"])
        source.setdefault("videos", []).append({
            "video_id": entry["video_id"],
            "title": entry["title"],
            "date": date,
            "channel_name": entry["channel_name"],
            "channel_id": entry["channel_id"],
            "channel_url": entry["channel_url"],
        })
        existing_ids.add(entry["video_id"])
        added_videos += 1
        print(f"[sync_playlist_videos] +video {entry['video_id']} ({entry['channel_name']}): {entry['title']}")

        policy = policies_by_url.get(entry["channel_url"])
        if policy is None:
            policy = {
                "channel_id": entry["channel_id"],
                "channel_name": entry["channel_name"],
                "channel_url": entry["channel_url"],
                "fetch_limit": 5,
                "retention": "selected",
                "selected_video_ids": [entry["video_id"]],
                "processing": "audio_and_frames",
                "id": f"{source['id']}:{entry['channel_id']}",
            }
            source.setdefault("channel_policies", []).append(policy)
            policies_by_url[entry["channel_url"]] = policy
            added_channels += 1
            print(f"[sync_playlist_videos] +channel {entry['channel_name']} (retention=selected)")
        elif policy.get("retention") == "selected":
            ids = policy.setdefault("selected_video_ids", [])
            if entry["video_id"] not in ids:
                ids.append(entry["video_id"])
                updated_selected += 1

    return {"added_videos": added_videos, "added_channels": added_channels, "updated_selected": updated_selected}


def main() -> int:
    sources_path = ROOT / "sources.json"
    config = json.loads(sources_path.read_text(encoding="utf-8"))
    totals = {"added_videos": 0, "added_channels": 0, "updated_selected": 0}
    for source in config.get("sources", []):
        if source.get("type") != "playlist":
            continue
        try:
            stats = sync_source(source)
        except RuntimeError as e:
            print(f"::warning::playlist sync failed for {source.get('id')}: {e}")
            continue
        for k in totals:
            totals[k] += stats[k]
    if totals["added_videos"]:
        sources_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[sync_playlist_videos] done. {totals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
