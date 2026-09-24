"""Scripted policies run offline. The language-model plug stays optional."""

from __future__ import annotations

from pathlib import Path

import pytest

from sietch.models import Assignment, Observation
from sietch.policies import LLMClientNotConfigured, LLMPolicy, ScriptedPolicy


def _obs() -> Observation:
    return Observation(
        tick=0,
        water=4,
        sheltered=False,
        storm=False,
        storm_in=None,
        base_integrity=3,
        shelter_locked=0,
        failure=None,
    )


def test_default_policy_does_not_need_a_client() -> None:
    decision = ScriptedPolicy().choose("eve", _obs(), Assignment(owner="eve", goal="maintain"))
    assert decision.kind == "handoff"
    assert decision.handoff is not None
    assert decision.handoff.missing_fields() == []


def test_llm_policy_without_a_client_raises() -> None:
    with pytest.raises(LLMClientNotConfigured):
        LLMPolicy().choose("eve", _obs(), Assignment(owner="eve", goal="maintain"))


def test_llm_policy_uses_an_injected_stub() -> None:
    class Stub:
        def complete(self, messages: list[dict[str, str]]) -> str:
            assert messages[0]["role"] == "system"
            return '{"action": "rest"}'

    decision = LLMPolicy(client=Stub()).choose(
        "eve", _obs(), Assignment(owner="eve", goal="maintain")
    )
    assert decision.action == "rest"


def test_llm_policy_rejects_unknown_actions() -> None:
    class Stub:
        def complete(self, messages: list[dict[str, str]]) -> str:
            return '{"action": "read_memory"}'

    with pytest.raises(ValueError):
        LLMPolicy(client=Stub()).choose("eve", _obs(), Assignment(owner="eve", goal="maintain"))


def test_runner_refuses_llm_config(tmp_path: Path) -> None:
    config = tmp_path / "llm.yaml"
    config.write_text(
        "mode: sandbox\nreal_game_connection: false\npolicy: llm\n"
        "policy_style: replan\nsupervisor:\n  human_present: true\n"
        "logging:\n  path: sessions/llm.jsonl\n",
        encoding="utf-8",
    )
    from sietch.session import run_from_config

    with pytest.raises(RuntimeError):
        run_from_config(config, operator_present=True, log_path=tmp_path / "out.jsonl")
