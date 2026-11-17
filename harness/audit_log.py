"""Append-only JSON-lines audit log with a hash chain.

Each record stores the hash of the previous record, so any change to an earlier
line breaks verification of every later line.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict


def _digest(prev_hash: str, payload: Dict[str, Any]) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((prev_hash + body).encode("utf-8")).hexdigest()


class AuditLog:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.prev_hash = "0" * 64
        if self.path.exists():
            lines = self.path.read_text().splitlines()
            if lines:
                self.prev_hash = json.loads(lines[-1])["hash"]

    def append(self, event: str, **fields: Any) -> str:
        payload = {"t": time.time(), "event": event, **fields}
        h = _digest(self.prev_hash, payload)
        record = {**payload, "prev": self.prev_hash, "hash": h}
        with self.path.open("a") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
        self.prev_hash = h
        return h


def verify(path: str | Path) -> bool:
    prev = "0" * 64
    for line in Path(path).read_text().splitlines():
        rec = json.loads(line)
        claimed = rec.pop("hash")
        if rec.pop("prev") != prev:
            return False
        if _digest(prev, rec) != claimed:
            return False
        prev = claimed
    return True
