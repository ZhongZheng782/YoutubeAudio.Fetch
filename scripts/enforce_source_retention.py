#!/usr/bin/env python3
"""Apply each source's selected/all/latest retention policy to repo artifacts."""
from __future__ import annotations

import json
import importlib.util
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "sources.json"
MANIFEST_PATH = ROOT / "audio_manifest.json"
METADATA_PATH = ROOT / "data/.video_metadata.json"
API = "https://api.github.com"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def video_ids_in_data(channel: str) -> set[str]:
    result: set[str] = set()
    folder = ROOT / "data" / channel
    if not folder.exists():
        return result
    prefix = f"{channel}_"
    for path in folder.iterdir():
        if not path.name.startswith(prefix):
            continue
        remainder = path.name[len(prefix):]
        video_id = remainder[:11]
        if VIDEO_ID_RE.fullmatch(video_id) and (len(remainder) == 11 or remainder[11] in "_."):
            result.add(video_id)
    return result


def release_api(repo: str, token: str):
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return session, f"{API}/repos/{repo}"


def delete_audio_release(session: requests.Session, repo_api: str, stem: str) -> None:
    tag = f"audio-{stem}"
    response = session.get(f"{repo_api}/releases/tags/{quote(tag, safe='')}")
    if response.status_code == 404:
        return
    response.raise_for_status()
    release_id = response.json()["id"]
    deleted = session.delete(f"{repo_api}/releases/{release_id}")
    if deleted.status_code not in {204, 404}:
        deleted.raise_for_status()
    ref = session.delete(f"{repo_api}/git/refs/tags/{quote(tag, safe='')}")
    if ref.status_code not in {204, 404}:
        ref.raise_for_status()


def latest_video_id(source: dict, repo: str, token: str) -> str | None:
    module_path = ROOT / "skills/skill-youtube-channel-fetch/scripts/channel_fetch.py"
    spec = importlib.util.spec_from_file_location("source_channel_fetch", module_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    fetcher = module.ChannelFetcher(source_repo=repo, token=token, repo_root=ROOT)
    videos = fetcher.list_channel_videos(source["url"], limit=1)
    return videos[0]["video_id"] if videos else None


def main() -> int:
    config = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8")) if METADATA_PATH.exists() else {}
    repo = os.environ.get("GITHUB_REPOSITORY", "ZhongZheng782/YoutubeAudio.Fetch")
    token = os.environ.get("GITHUB_TOKEN", "")

    by_directory: dict[str, list[dict]] = {}
    for source in config.get("sources", []):
        by_directory.setdefault(source["channel_dir"], []).append(source)

    session, repo_api = release_api(repo, token) if token else (None, "")
    config_changed = False
    for channel, sources in by_directory.items():
        modes = {source.get("retention", "all") for source in sources}
        if modes == {"all"}:
            continue
        if len(modes) != 1:
            print(f"::warning::retention conflict for {channel}; keeping all files")
            continue
        mode = next(iter(modes))
        existing_ids = {
            stem[-11:] for stem in manifest
            if stem[:-12] == channel and len(stem) >= 12
        } | video_ids_in_data(channel)
        if mode == "selected":
            keep_ids = {
                video_id
                for source in sources
                for video_id in source.get("selected_video_ids", [])
            }
            keep_ids &= existing_ids
        elif mode == "latest":
            source = next((item for item in sources if item.get("type") == "playlist"), sources[0])
            try:
                newest_id = latest_video_id(source, repo, token)
            except Exception as exc:
                print(f"::warning::cannot determine latest video for {channel}: {exc}; keeping all files")
                continue
            if not newest_id:
                print(f"::warning::no latest video found for {channel}; keeping all files")
                continue
            keep_ids = {newest_id}
            for source in sources:
                source["latest_video_id"] = newest_id
            config_changed = True
        else:
            print(f"::warning::unknown retention mode {mode!r} for {channel}; keeping all files")
            continue

        remove_ids = existing_ids - keep_ids
        if mode == "selected" and not keep_ids:
            print(f"::warning::selected mode has no existing selected videos for {channel}; keeping all files")
            continue
        if not remove_ids:
            continue
        if not token:
            print(f"::warning::GITHUB_TOKEN missing; cannot prune audio releases for {channel}")
            continue

        remove_stems = [stem for stem in manifest if stem[:-12] == channel and stem[-11:] in remove_ids]
        for stem in remove_stems:
            delete_audio_release(session, repo_api, stem)
            manifest.pop(stem, None)

        folder = ROOT / "data" / channel
        if folder.exists():
            for path in folder.iterdir():
                prefix = f"{channel}_"
                remainder = path.name[len(prefix):] if path.name.startswith(prefix) else ""
                video_id = remainder[:11]
                if VIDEO_ID_RE.fullmatch(video_id) and (len(remainder) == 11 or remainder[11] in "_.") and video_id in remove_ids:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
        for video_id in remove_ids:
            metadata.pop(video_id, None)
        print(f"[source retention] {channel}: retained {len(keep_ids)} video(s), removed {len(remove_ids)}")

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    if METADATA_PATH.exists():
        METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    if config_changed:
        SOURCES_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
