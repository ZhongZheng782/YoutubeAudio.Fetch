#!/usr/bin/env python3
"""Generate a freshness-monitorable CSV from audio_manifest.json."""
import csv, json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "audio_manifest.json"
METADATA = ROOT / "data" / ".video_metadata.json"
OUTPUT = ROOT / "raw_youtube_audio_manifest.csv"
CST = timezone(timedelta(hours=8))

def now_cst():
    return datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST")

def main():
    process_ts = now_cst()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    metadata = json.loads(METADATA.read_text(encoding="utf-8")) if METADATA.exists() else {}
    rows = []
    for stem, audio_url in sorted(manifest.items()):
        video_id = next((key for key in metadata if stem.endswith("_" + key)), "")
        meta = metadata.get(video_id, {})
        published = str(meta.get("date", ""))
        updated = f"{published} 00:00:00 CST" if published else process_ts
        rows.append({
            "video_id": video_id,
            "title": meta.get("title", stem),
            "channel_name": meta.get("channel_name", stem.rsplit("_", 1)[0]),
            "published_at": published,
            "stem": stem,
            "audio_url": audio_url,
            "audio_status": "available" if audio_url else "missing",
            "updated_timestamp": updated,
            "process_timestamp": process_ts,
        })
    fields = ["video_id", "title", "channel_name", "published_at", "stem", "audio_url", "audio_status", "updated_timestamp", "process_timestamp"]
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUTPUT}")

if __name__ == "__main__":
    main()
