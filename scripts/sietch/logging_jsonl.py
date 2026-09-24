"""Append-only JSONL session log.

Each line is one JSON object. The sandbox schema is sietch.session.v1.
The writer refuses keys that would carry personal data or secrets.
Log files belong under sessions/ and are gitignored.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "sietch.session.v1"

LOG_EVENTS = frozenset(
    {
        "session_start",
        "decision",
        "handoff_accepted",
        "handoff_rejected",
        "approval_requested",
        "approval_granted",
        "approval_denied",
        "substituted_rest",
        "action_result",
        "kill_switch",
        "session_end",
    }
)

FORBIDDEN_KEYS = frozenset(
    {
        "email",
        "phone",
        "phone_number",
        "ip",
        "ip_address",
        "player_name",
        "real_name",
        "address",
        "password",
        "passwd",
        "token",
        "api_key",
        "secret",
        "credential",
    }
)


class PersonalDataRejected(ValueError):
    """Raised when a log record contains a forbidden key."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _reject_personal(value: object, path: str = "") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            name = str(key).lower()
            if name in FORBIDDEN_KEYS:
                where = f"{path}.{name}" if path else name
                raise PersonalDataRejected(
                    f"Refusing to write log field '{where}'. "
                    "Sandbox logs do not store personal data or secrets."
                )
            _reject_personal(item, name if not path else f"{path}.{name}")
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_personal(item, path)


class JsonlLogger:
    """Write one JSON object per line. The clock is injectable for tests."""

    def __init__(
        self,
        path: Path,
        session_id: str,
        clock: Callable[[], str] | None = None,
    ) -> None:
        self.path = Path(path)
        self.session_id = session_id
        self.clock = clock or _now
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: str, **fields: object) -> dict[str, object]:
        record: dict[str, object] = {
            "schema": SCHEMA,
            "ts": self.clock(),
            "session_id": self.session_id,
            "event": event,
        }
        record.update(fields)
        _reject_personal(record)
        if event not in LOG_EVENTS:
            raise ValueError(f"Unknown log event '{event}'. Add it to LOG_EVENTS and the spec together.")
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, default=str) + "\n")
        return record

    def read(self) -> list[dict[str, object]]:
        if not self.path.exists():
            return []
        lines = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                lines.append(json.loads(line))
        return lines
