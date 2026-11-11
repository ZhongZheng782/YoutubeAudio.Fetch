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


def latest_video_id(channel_url: str, repo: str, token: str) -> str | None:
    module_path = ROOT / "skills/skill-youtube-channel-fetch/scripts/channel_fetch.py"
    spec = importlib.util.spec_from_file_location("source_channel_fetch", module_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    fetcher = module.ChannelFetcher(source_repo=repo, token=token, repo_root=ROOT)
    videos = fetcher.list_channel_videos(channel_url, limit=1)
    return videos[0]["video_id"] if videos else None


def source_video_ids(manifest: dict, channel_dir: str) -> set[str]:
    return {
        stem[-11:] for stem in manifest
        if len(stem) >= 12 and stem[:-12] == channel_dir
    } | video_ids_in_data(channel_dir)


def apply_retention(channel_dir: str, policy: dict, manifest: dict, metadata: dict,
                    session: requests.Session | None, repo_api: str, repo: str, token: str,
                    channel_url: str | None = None) -> bool:
    mode = policy.get("retention", "all")
    if mode == "all":
        return False
    filter_channel_url = channel_url

    existing_ids = source_video_ids(manifest, channel_dir)
    if channel_url:
        # The playlist data folder contains videos from several uploaders. Limit this
        # policy to the selected uploader so other channel groups remain untouched.
        owned_ids = {
            video_id for video_id in existing_ids
            if metadata.get(video_id, {}).get("channel_url") == channel_url
        }
        owned_ids.update(policy.get("selected_video_ids", []))
    else:
        owned_ids = existing_ids

    if mode == "selected":
        keep_ids = set(policy.get("selected_video_ids", []))
        if not keep_ids:
            print(f"::warning::selected mode has no video IDs for {policy.get('channel_name', channel_dir)}; keeping all files")
            return False
    elif mode == "since_date":
        date_after = policy.get("date_after")
        if not date_after:
            print(f"::warning::since_date mode has no date_after for {policy.get('channel_name', channel_dir)}; keeping all files")
            return False
        # Keep metadata-less files conservatively; remove only videos with a known
        # upload date before the inclusive cutoff.
        keep_ids = {
            video_id for video_id in owned_ids
            if not metadata.get(video_id, {}).get("date") or metadata[video_id]["date"] >= date_after
        }
    elif mode == "latest":
        latest_url = channel_url or policy.get("url")
        try:
            newest_id = latest_video_id(latest_url, repo, token) if latest_url else None
        except Exception as exc:
            print(f"::warning::cannot determine latest video for {policy.get('channel_name', channel_dir)}: {exc}; keeping all files")
            return False
        if not newest_id:
            print(f"::warning::no latest video found for {policy.get('channel_name', channel_dir)}; keeping all files")
            return False
        keep_ids = {newest_id}
        if policy.get("latest_video_id") != newest_id:
            policy["latest_video_id"] = newest_id
            config_changed = True
        else:
            config_changed = False
    else:
        print(f"::warning::unknown retention mode {mode!r}; keeping all files")
        return False

    remove_ids = owned_ids - keep_ids
    if not remove_ids:
        return locals().get("config_changed", False)
    if not token or session is None:
        print(f"::warning::GITHUB_TOKEN missing; cannot prune audio releases for {policy.get('channel_name', channel_dir)}")
        return locals().get("config_changed", False)

    remove_stems = [
        stem for stem in manifest
        if len(stem) >= 12 and stem[:-12] == channel_dir and stem[-11:] in remove_ids
    ]
    for stem in remove_stems:
        delete_audio_release(session, repo_api, stem)
        manifest.pop(stem, None)

    folder = ROOT / "data" / channel_dir
    if folder.exists():
        prefix = f"{channel_dir}_"
        for path in folder.iterdir():
            remainder = path.name[len(prefix):] if path.name.startswith(prefix) else ""
            video_id = remainder[:11]
            if VIDEO_ID_RE.fullmatch(video_id) and (len(remainder) == 11 or remainder[11] in "_.") and video_id in remove_ids:
                if filter_channel_url and metadata.get(video_id, {}).get("channel_url") != filter_channel_url:
                    continue
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
    for video_id in remove_ids:
        if not filter_channel_url or metadata.get(video_id, {}).get("channel_url") == filter_channel_url:
            metadata.pop(video_id, None)
    print(f"[source retention] {policy.get('channel_name', channel_dir)}: retained {len(keep_ids)} video(s), removed {len(remove_ids)}")
    return locals().get("config_changed", False)


def main() -> int:
    config = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8")) if METADATA_PATH.exists() else {}
    repo = os.environ.get("GITHUB_REPOSITORY", "ZhongZheng782/YoutubeAudio.Fetch")
    token = os.environ.get("GITHUB_TOKEN", "")

    session, repo_api = release_api(repo, token) if token else (None, "")
    config_changed = False
    for source in config.get("sources", []):
        if source.get("type") == "channel":
            config_changed |= apply_retention(source["channel_dir"], source, manifest, metadata,
                                               session, repo_api, repo, token)
        elif source.get("type") == "playlist":
            for policy in source.get("channel_policies", []):
                config_changed |= apply_retention(source["channel_dir"], policy, manifest, metadata,
                                                   session, repo_api, repo, token,
                                                   channel_url=policy.get("channel_url"))

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    if METADATA_PATH.exists():
        METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    if config_changed:
        SOURCES_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
