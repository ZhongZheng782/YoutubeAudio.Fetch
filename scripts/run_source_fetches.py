#!/usr/bin/env python3
"""Fetch configured YouTube sources using their per-source policies."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
FETCHER = ROOT / "skills/skill-youtube-channel-fetch/scripts/channel_fetch.py"
INCREMENTAL_FETCH_LIMIT = 25
YOUTUBE_API_ROOT = "https://www.googleapis.com/youtube/v3"
YOUTUBE_HANDLE_RE = re.compile(r"youtube\.com/@([^/?]+)", re.IGNORECASE)
YOUTUBE_CHANNEL_ID_RE = re.compile(r"youtube\.com/channel/(UC[A-Za-z0-9_-]+)", re.IGNORECASE)


def list_uploads(policy: dict, api_key: str, mode: str) -> tuple[list[dict], str, str, str]:
    """List this channel's uploads, stopping at the saved cursor or date cutoff."""
    channel_id = policy.get("youtube_channel_id") or policy.get("channel_id")
    uploads_id = policy.get("youtube_uploads_playlist_id")

    def api_get(endpoint: str, **params: str) -> dict:
        response = requests.get(
            f"{YOUTUBE_API_ROOT}/{endpoint}",
            params={**params, "key": api_key}, timeout=30,
        )
        if response.status_code >= 400:
            raise RuntimeError(f"YouTube API {endpoint} returned HTTP {response.status_code}: {response.text[:300]}")
        return response.json()

    if not uploads_id:
        if channel_id and channel_id.startswith("UC"):
            channel = api_get("channels", part="contentDetails", id=channel_id)
        else:
            handle_match = YOUTUBE_HANDLE_RE.search(policy["channel_url"])
            channel_match = YOUTUBE_CHANNEL_ID_RE.search(policy["channel_url"])
            if handle_match:
                channel = api_get("channels", part="contentDetails", forHandle=handle_match.group(1))
            elif channel_match:
                channel = api_get("channels", part="contentDetails", id=channel_match.group(1))
            else:
                raise ValueError(f"cannot resolve channel ID from {policy['channel_url']}")
        items = channel.get("items", [])
        if not items:
            raise ValueError(f"YouTube channel not found: {policy['channel_url']}")
        channel_id = items[0]["id"]
        uploads_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    cutoff = policy.get("date_after") if mode == "since_date" else None
    scope = "all" if mode == "all" else f"since_date:{cutoff}"
    completed_scope = policy.get("sync_completed_scope")
    cursor_scope = policy.get("youtube_sync_scope")
    cursor = policy.get("youtube_sync_cursor") if scope in {completed_scope, cursor_scope} else None
    # `all` means retain the existing archive and keep up with uploads. It does
    # not trigger a historical channel crawl; seed the cursor from the newest item.
    seed_cursor = mode == "all" and not cursor
    first_page_only = seed_cursor or (completed_scope == scope and not cursor)
    entries: list[dict] = []
    page_token = ""
    newest_id = ""
    cursor_found = False
    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": uploads_id,
            "maxResults": "1" if seed_cursor else "50",
        }
        if page_token:
            params["pageToken"] = page_token
        page = api_get("playlistItems", **params)
        for item in page.get("items", []):
            snippet = item.get("snippet", {})
            video_id = snippet.get("resourceId", {}).get("videoId")
            if not video_id:
                continue
            if not newest_id:
                newest_id = video_id
            if cursor and video_id == cursor:
                cursor_found = True
                break
            published = item.get("contentDetails", {}).get("videoPublishedAt") or snippet.get("publishedAt", "")
            published_date = published[:10] if len(published) >= 10 else ""
            if cutoff and published_date and published_date < cutoff:
                # Initial date backfill is newest-first; older pages are out of scope.
                if not cursor:
                    cursor_found = True
                    break
                continue
            entries.append({
                "video_id": video_id,
                "title": snippet.get("title") or video_id,
                "channel": snippet.get("videoOwnerChannelTitle") or policy.get("channel_name") or "channel",
            })
        if cursor_found or first_page_only:
            break
        page_token = page.get("nextPageToken", "")
        if not page_token:
            break
    return entries, channel_id, uploads_id, newest_id or cursor or ""


def main() -> int:
    override = sys.argv[1] if len(sys.argv) > 1 else ""
    config = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    metadata_path = ROOT / "data/.video_metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    for source in config.get("sources", []):
        if source.get("type") not in {"channel", "playlist"}:
            continue
        if source["type"] == "channel":
            run_policy(source, source, override)
            continue

        policies = {policy.get("channel_url"): policy for policy in source.get("channel_policies", [])}
        derived: dict[str, dict] = {}
        for video in source.get("videos", []):
            video_id = video.get("video_id", "")
            meta = metadata.get(video_id, {})
            channel_url = video.get("channel_url") or meta.get("channel_url")
            if not channel_url:
                print(f"::warning::no uploader channel URL for playlist video {video_id}; skipping")
                continue
            channel_id = video.get("channel_id") or meta.get("channel_id") or channel_url.rstrip("/").split("/")[-1]
            policy = derived.setdefault(channel_url, {
                "id": f"{source['id']}:{channel_id}",
                "channel_id": channel_id,
                "channel_name": video.get("channel_name") or meta.get("channel_name") or channel_id,
                "channel_url": channel_url,
                "retention": "selected",
                "selected_video_ids": [],
                "fetch_limit": source.get("fetch_limit", 5),
                "processing": "audio_and_frames",
            })
            policy["selected_video_ids"].append(video_id)
        for channel_url, default_policy in derived.items():
            policy = policies.get(channel_url, default_policy)
            if policy.get("retention") == "selected" and not policy.get("selected_video_ids"):
                policy["selected_video_ids"] = default_policy["selected_video_ids"]
            policy.setdefault("fetch_limit", source.get("fetch_limit", 5))
            policy.setdefault("id", f"{source['id']}:{policy.get('channel_id', channel_url)}")
            run_policy(source, policy, override)

        for channel_url, policy in policies.items():
            if channel_url not in derived:
                run_policy(source, policy, override)
    (ROOT / "sources.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return 0


def run_policy(source: dict, policy: dict, override: str) -> None:
    mode = policy.get("retention", "latest")
    if mode == "since_date" and not policy.get("date_after"):
        print(f"::warning::since_date mode has no date_after for {policy['id']}; skipping")
        return
    configured_limit = int(override or policy.get("fetch_limit", source.get("fetch_limit", 5)))
    limit = 1 if mode == "latest" else configured_limit
    scope = "all" if mode == "all" else f"since_date:{policy.get('date_after', '')}"
    already_scanned = policy.get("sync_completed_scope") == scope
    cursor_initialized = policy.get("youtube_sync_scope") == scope
    incremental = (already_scanned or cursor_initialized) and mode in {"all", "since_date"} and not override
    if incremental:
        limit = max(limit, INCREMENTAL_FETCH_LIMIT)
    command = [
        sys.executable, str(FETCHER), "fetch", policy.get("channel_url", source["url"]),
        "--source-slug", source["channel_dir"],
        "--sync",
    ]
    api_key = os.environ.get("YOUTUBE_DATA_API_KEY", "").strip()
    api_entries = None
    api_state = None
    if api_key and mode in {"all", "since_date"} and not override:
        try:
            api_entries, channel_id, uploads_id, newest_id = list_uploads(policy, api_key, mode)
            api_state = (channel_id, uploads_id, newest_id)
        except Exception as exc:
            print(f"::warning::YouTube Data API listing failed for {policy['id']} ({type(exc).__name__}); falling back to yt-dlp", flush=True)

    video_list_path = None
    if api_entries is not None:
        video_list = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".json", prefix="youtube-uploads-", delete=False
        )
        try:
            json.dump(api_entries, video_list, ensure_ascii=False)
            video_list.close()
            video_list_path = Path(video_list.name)
            command.extend(["--video-list", str(video_list_path)])
        except Exception:
            video_list.close()
            Path(video_list.name).unlink(missing_ok=True)
            raise
    if mode == "all" and not incremental and not override:
        if api_entries is None:
            command.extend(["--limit", "1"])
    elif mode == "since_date":
        date_after = policy.get("date_after")
        if not incremental and api_entries is None:
            command.extend(["--date-after", date_after])
        if api_entries is None and (incremental or override):
            command.extend(["--limit", str(limit)])
    elif api_entries is None:
        command.extend(["--limit", str(limit)])
    if mode == "selected":
        selected = policy.get("selected_video_ids", [])
        if not selected:
            print(f"[run_source_fetches] {policy['id']}: selected mode has no video IDs; skipping")
            return
        command = [*command, *(arg for video_id in selected for arg in ("--video-id", video_id))]

    print(f"[run_source_fetches] fetching {policy.get('channel_name', source['name'])} ({mode})", flush=True)
    try:
        result = subprocess.run(command, cwd=ROOT)
    finally:
        if video_list_path:
            video_list_path.unlink(missing_ok=True)
    if result.returncode:
        print(f"::warning::fetch failed for {policy['id']} (exit {result.returncode})")
    elif api_state:
        channel_id, uploads_id, newest_id = api_state
        policy["youtube_channel_id"] = channel_id
        policy["youtube_uploads_playlist_id"] = uploads_id
        if newest_id:
            policy["youtube_sync_cursor"] = newest_id
        if mode == "all" and not override:
            policy["youtube_sync_scope"] = scope
        elif mode == "since_date" and not override:
            policy["sync_completed_scope"] = scope
            policy["youtube_sync_scope"] = scope
        print(f"[run_source_fetches] {policy['id']}: playlist sync processed {len(api_entries)} videos", flush=True)
    elif mode in {"all", "since_date"} and not override and not already_scanned:
        if mode == "all":
            policy["youtube_sync_scope"] = scope
            print(f"[run_source_fetches] {policy['id']}: newest-video cursor initialized", flush=True)
        else:
            policy["sync_completed_scope"] = scope
            policy["youtube_sync_scope"] = scope
            print(f"[run_source_fetches] {policy['id']}: initial scan completed for {scope}", flush=True)
    elif incremental:
        print(f"[run_source_fetches] {policy['id']}: incremental scan limit={limit}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
