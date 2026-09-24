"""JSONL logs stay structured and refuse personal-data fields."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sietch.logging_jsonl import LOG_EVENTS, JsonlLogger, PersonalDataRejected, SCHEMA
from sietch.orchestrator import run_session


def test_lines_are_json_objects_with_the_schema(tmp_path: Path) -> None:
    path = tmp_path / "session.jsonl"
    report = run_session(
        session_id="log-1",
        operator_present=True,
        log_path=path,
        max_steps=6,
        clock=lambda: "2026-09-24T00:00:00+00:00",
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines
    events = []
    for line in lines:
        record = json.loads(line)
        assert record["schema"] == SCHEMA
        assert record["session_id"] == "log-1"
        assert record["ts"] == "2026-09-24T00:00:00+00:00"
        events.append(record["event"])
    assert events[0] == "session_start"
    assert events[-1] == "session_end"
    assert "handoff_accepted" in events
    assert report.steps == 6
    assert set(events) <= LOG_EVENTS


def test_personal_data_keys_are_refused(tmp_path: Path) -> None:
    logger = JsonlLogger(tmp_path / "blocked.jsonl", "s", clock=lambda: "t")
    with pytest.raises(PersonalDataRejected):
        logger.write("decision", email="redacted")
    assert logger.read() == []


def test_two_runs_share_an_action_trace(tmp_path: Path) -> None:
    def trace(name: str) -> list[tuple[object, ...]]:
        path = tmp_path / f"{name}.jsonl"
        run_session(
            session_id=name,
            operator_present=True,
            log_path=path,
            max_steps=16,
            clock=lambda: "2026-09-24T00:00:00+00:00",
        )
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            if record["event"] == "action_result":
                rows.append(
                    (
                        record["action"],
                        record["tick"],
                        record["failure"],
                        record["water"],
                        record["agent"],
                    )
                )
        return rows

    assert trace("a") == trace("b")
