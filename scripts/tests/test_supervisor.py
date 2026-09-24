"""Presence, the approval gate, and the kill switch."""

from __future__ import annotations

from pathlib import Path

import pytest

from sietch.models import HIGH_IMPACT_ACTIONS
from sietch.orchestrator import run_session
from sietch.policies import ScriptedPolicy
from sietch.supervisor import OperatorAbsentError, Supervisor


def test_supervisor_requires_a_human() -> None:
    with pytest.raises(OperatorAbsentError):
        Supervisor(human_present=False)


def test_default_approver_denies_high_impact() -> None:
    supervisor = Supervisor(human_present=True)
    assert supervisor.review("gather_water") is True
    assert supervisor.review("discard_water") is False
    assert "abandon_shelter" in HIGH_IMPACT_ACTIONS


def test_denied_high_impact_action_is_not_applied(tmp_path: Path) -> None:
    report = run_session(
        session_id="deny",
        operator_present=True,
        log_path=tmp_path / "deny.jsonl",
        max_steps=1,
        policies={
            "eve": ScriptedPolicy(force_action="discard_water"),
            "edos": ScriptedPolicy(),
        },
        clock=lambda: "2026-09-24T00:00:00+00:00",
    )
    assert report.approval_blocks == 1
    assert report.final_water > 0
    assert all(item["failure"] != "water_discarded" for item in report.failures)


def test_approved_high_impact_action_is_applied(tmp_path: Path) -> None:
    report = run_session(
        session_id="allow",
        operator_present=True,
        log_path=tmp_path / "allow.jsonl",
        max_steps=1,
        approver=lambda _action: True,
        policies={
            "eve": ScriptedPolicy(force_action="discard_water"),
            "edos": ScriptedPolicy(),
        },
        clock=lambda: "2026-09-24T00:00:00+00:00",
    )
    assert report.approval_blocks == 0
    assert report.failures[0]["failure"] == "water_discarded"
    assert report.final_water == 0


def test_kill_switch_stops_the_loop(tmp_path: Path) -> None:
    def stop(supervisor: Supervisor) -> None:
        if supervisor.decisions_seen >= 3:
            supervisor.kill()

    report = run_session(
        session_id="kill",
        operator_present=True,
        log_path=tmp_path / "kill.jsonl",
        max_steps=16,
        before_decision=stop,
        clock=lambda: "2026-09-24T00:00:00+00:00",
    )
    assert report.killed is True
    assert report.steps < 16
    text = (tmp_path / "kill.jsonl").read_text(encoding="utf-8").strip().splitlines()
    events = [__import__("json").loads(line)["event"] for line in text]
    assert "kill_switch" in events
    assert events[-1] == "session_end"
    assert events.index("kill_switch") < events.index("session_end")


def test_session_refuses_to_start_without_operator(tmp_path: Path) -> None:
    log_path = tmp_path / "absent.jsonl"
    with pytest.raises(OperatorAbsentError):
        run_session(
            session_id="absent",
            operator_present=False,
            human_present=True,
            log_path=log_path,
        )
    assert not log_path.exists()
