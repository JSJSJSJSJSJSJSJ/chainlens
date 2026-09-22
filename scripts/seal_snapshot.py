"""Seal a manually reviewed candidate's excerpts and manifest; never fetch sources.

Usage: uv run python scripts/seal_snapshot.py candidate.json --manifest manifest.json
Does not change factual/review status or retrieval dates. Existing published
snapshots must be preserved under their own versions; use a new filename/version.
"""
import argparse
import hashlib
import json
from pathlib import Path

from app.schemas import Snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.snapshot.read_text(encoding="utf-8"))
    for item in payload["evidence"]:
        item["content_sha256"] = hashlib.sha256(item["excerpt"].encode("utf-8")).hexdigest()
    Snapshot.model_validate(payload)
    raw = (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    args.snapshot.write_bytes(raw)
    manifest = {key: payload["metadata"][key] for key in ("dataset_version", "research_cutoff", "score_version")}
    manifest.update(snapshot_file=args.snapshot.name, snapshot_sha256=hashlib.sha256(raw).hexdigest(),
                    counts={key: len(payload[key]) for key in ("companies", "relationships", "evidence")})
    args.manifest.write_bytes((json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
