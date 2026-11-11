#!/usr/bin/env python3
"""Fetch configured YouTube sources using their per-source policies."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FETCHER = ROOT / "skills/skill-youtube-channel-fetch/scripts/channel_fetch.py"


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
    return 0


def run_policy(source: dict, policy: dict, override: str) -> None:
    mode = policy.get("retention", "all")
    configured_limit = int(override or policy.get("fetch_limit", source.get("fetch_limit", 5)))
    limit = 1 if mode == "latest" else configured_limit
    command = [
        sys.executable, str(FETCHER), "fetch", policy.get("channel_url", source["url"]),
        "--source-slug", source["channel_dir"],
        "--sync",
    ]
    if mode == "all" and not override:
        command.append("--all")
    else:
        command.extend(["--limit", str(limit)])
    if mode == "selected":
        selected = policy.get("selected_video_ids", [])
        if not selected:
            print(f"[run_source_fetches] {policy['id']}: selected mode has no video IDs; skipping")
            return
        command = [*command, *(arg for video_id in selected for arg in ("--video-id", video_id))]

    print(f"[run_source_fetches] fetching {policy.get('channel_name', source['name'])} ({mode})", flush=True)
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        print(f"::warning::fetch failed for {policy['id']} (exit {result.returncode})")


if __name__ == "__main__":
    raise SystemExit(main())
