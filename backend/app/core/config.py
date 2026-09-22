"""Resolve defaults relative to the repository, independent of the working directory."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SNAPSHOT = ROOT / "data" / "snapshots" / "2026-09-16.v1.json"


def database_url() -> str:
    return os.environ.get(
        "CHAINLENS_DATABASE_URL", f"sqlite:///{ROOT / 'data' / 'chainlens.sqlite3'}"
    )


def snapshot_path() -> Path:
    return Path(os.environ.get("CHAINLENS_SNAPSHOT", str(DEFAULT_SNAPSHOT))).resolve()
