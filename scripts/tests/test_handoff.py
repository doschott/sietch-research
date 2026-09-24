"""Complete handoffs move the task. Incomplete handoffs do not."""

from __future__ import annotations

from pathlib import Path

from sietch.models import HandoffRecord
from sietch.orchestrator import run_session
from sietch.policies import ScriptedPolicy


def test_missing_fields_are_named() -> None:
    record = HandoffRecord(
        from_agent="eve",
        to_agent="edos",
        goal="recover",
        reason="",
        world_snapshot=None,
        open_commitments=None,
        failure_history=None,
    )
    missing = record.missing_fields()
    assert "reason" in missing
    assert "world_snapshot" in missing
    assert "open_commitments" in missing
    assert "failure_history" in missing


def test_complete_handoff_is_accepted(tmp_path: Path) -> None:
    report = run_session(
        session_id="complete",
        operator_present=True,
        log_path=tmp_path / "complete.jsonl",
        max_steps=8,
        clock=lambda: "2026-09-24T00:00:00+00:00",
    )
    assert report.handoffs_accepted >= 1
    assert report.handoffs_rejected == 0


def test_minimal_handoff_is_rejected_and_owner_stays(tmp_path: Path) -> None:
    report = run_session(
        session_id="minimal",
        operator_present=True,
        log_path=tmp_path / "minimal.jsonl",
        max_steps=4,
        policies={
            "eve": ScriptedPolicy(handoff_style="minimal"),
            "edos": ScriptedPolicy(handoff_style="minimal"),
        },
        clock=lambda: "2026-09-24T00:00:00+00:00",
    )
    assert report.handoffs_accepted == 0
    assert report.handoffs_rejected >= 1
    assert report.final_owner == "eve"
