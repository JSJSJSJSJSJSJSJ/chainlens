"""Offline snapshot inventory, integrity validation and comparison; no network I/O.

Online discovery and verification are deliberate research steps documented in
docs/methodology.md. This tool never converts a fetched page into a factual claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data" / "snapshots" / "2026-09-16.v1.json"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprint(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def verify(path: Path, manifest_path: Path | None) -> dict:
    snapshot = read(path)
    failures: list[str] = []
    for category in ("companies", "relationships", "evidence"):
        ids = [item["id"] for item in snapshot[category]]
        if len(ids) != len(set(ids)):
            failures.append(f"Duplicate IDs in {category}")
    for evidence in snapshot["evidence"]:
        digest = hashlib.sha256(evidence["excerpt"].encode("utf-8")).hexdigest()
        if digest != evidence["content_sha256"]:
            failures.append(f"Excerpt checksum mismatch: {evidence['id']}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if manifest_path:
        manifest = read(manifest_path)
        if manifest["snapshot_sha256"] != digest:
            failures.append("Snapshot file checksum mismatch")
        for key in ("dataset_version", "research_cutoff", "score_version"):
            if manifest[key] != snapshot["metadata"][key]:
                failures.append(f"Manifest metadata mismatch: {key}")
        if manifest["snapshot_file"] != path.name:
            failures.append("Manifest filename mismatch")
        for key, expected in manifest["counts"].items():
            if len(snapshot[key]) != expected:
                failures.append(f"Manifest count mismatch: {key}")
    return {"valid": not failures, "snapshot_sha256": digest,
            "counts": {key: len(snapshot[key]) for key in ("companies", "relationships", "evidence")},
            "failures": failures}


def compare(old: dict, new: dict) -> dict:
    result = {"old_version": old["metadata"]["dataset_version"],
              "new_version": new["metadata"]["dataset_version"], "changes": {}}
    for category in ("companies", "relationships", "evidence"):
        before = {item["id"]: item for item in old[category]}
        after = {item["id"]: item for item in new[category]}
        result["changes"][category] = {
            "added": sorted(after.keys() - before.keys()),
            "removed": sorted(before.keys() - after.keys()),
            "modified": sorted(key for key in before.keys() & after.keys()
                               if fingerprint(before[key]) != fingerprint(after[key])),
        }
    return result


def inventory(snapshot: dict) -> dict:
    sources: dict[str, dict] = {}
    for item in snapshot["evidence"]:
        source = sources.setdefault(item["source_url"], {
            key: item[key] for key in ("source_url", "publisher", "published_at", "retrieved_at",
                                      "access_restrictions", "redistribution_notes")
        })
        source.setdefault("evidence_ids", []).append(item["id"])
    return {"dataset_version": snapshot["metadata"]["dataset_version"], "sources": list(sources.values())}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("verify", help="Check snapshot and excerpt hashes (offline)")
    validate.add_argument("snapshot", type=Path, nargs="?", default=DEFAULT)
    validate.add_argument("--manifest", type=Path)
    listing = sub.add_parser("sources", help="Print the reproducible source inventory")
    listing.add_argument("snapshot", type=Path, nargs="?", default=DEFAULT)
    diff = sub.add_parser("compare", help="Compare immutable old and candidate snapshots")
    diff.add_argument("old", type=Path)
    diff.add_argument("new", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "verify":
            result = verify(args.snapshot, args.manifest)
        elif args.command == "compare":
            result = compare(read(args.old), read(args.new))
        else:
            result = inventory(read(args.snapshot))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"Snapshot error: {exc}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.command == "verify" and not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
