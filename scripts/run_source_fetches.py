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
    for source in config.get("sources", []):
        if source.get("type") not in {"channel", "playlist"}:
            continue
        mode = source.get("retention", "all")
        limit = 1 if mode == "latest" else int(override or source.get("fetch_limit", 5))
        command = [
            sys.executable, str(FETCHER), "fetch", source["url"],
            "--source-slug", source["channel_dir"],
            "--limit", str(limit), "--sync",
        ]
        if mode == "selected":
            selected = source.get("selected_video_ids", [])
            if not selected:
                print(f"[run_source_fetches] {source['id']}: selected mode has no video IDs; skipping")
                continue
            command = [*command, *(arg for video_id in selected for arg in ("--video-id", video_id))]

        print(f"[run_source_fetches] fetching {source['type']} {source['id']} ({mode})", flush=True)
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            print(f"::warning::fetch failed for {source['id']} (exit {result.returncode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
