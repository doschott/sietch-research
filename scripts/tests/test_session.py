"""Config loading, the command-line runner, and the registered scenario."""

from __future__ import annotations

from pathlib import Path

import pytest

from sietch.config import load_config
from sietch.evaluate import run_registered
from sietch.guard import RealGameConnectionDisabled
from sietch.session import main

ROOT = Path(__file__).resolve().parents[1]
SANDBOX = ROOT / "configs" / "sandbox.yaml"
RETRY = ROOT / "configs" / "sandbox-retry.yaml"


def test_sandbox_template_stays_offline() -> None:
    config = load_config(SANDBOX)
    assert config.mode == "sandbox"
    assert config.real_game_connection is False
    assert config.policy_name == "scripted"
    assert config.policy_style == "replan"
    assert config.human_present is True
    assert config.world.seed == 7


def test_retry_template_matches_the_same_world() -> None:
    replan = load_config(SANDBOX)
    retry = load_config(RETRY)
    assert retry.policy_style == "retry"
    assert retry.world == replan.world


def test_real_game_flag_in_yaml_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        "mode: sandbox\nreal_game_connection: true\npolicy: scripted\n"
        "supervisor:\n  human_present: true\n",
        encoding="utf-8",
    )
    with pytest.raises(RealGameConnectionDisabled):
        load_config(path)


def test_cli_requires_the_operator_flag(tmp_path: Path) -> None:
    code = main(["--config", str(SANDBOX), "--log", str(tmp_path / "nope.jsonl"), "--steps", "2"])
    assert code == 2
    assert not (tmp_path / "nope.jsonl").exists()


def test_cli_runs_offline(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    log_path = tmp_path / "cli.jsonl"
    code = main(
        [
            "--config",
            str(SANDBOX),
            "--operator-present",
            "--log",
            str(log_path),
            "--steps",
            "4",
            "--seed",
            "7",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    assert "style=replan" in captured.out
    assert log_path.exists()


def test_registered_scenario_orders_recovery(tmp_path: Path) -> None:
    """Lock the scenario v1 fingerprint. Update methodology/evaluation.md with it."""
    replan = run_registered("replan", tmp_path / "replan.jsonl")
    retry = run_registered("retry", tmp_path / "retry.jsonl")
    assert replan.steps == 16
    assert replan.handoffs_accepted == 4
    assert replan.handoffs_rejected == 0
    assert [item["failure"] for item in replan.failures] == ["exposure"]
    assert replan.recovery_latencies == [1]
    assert replan.unrecovered_failures == 0
    assert replan.approval_blocks == 0
    assert replan.killed is False
    assert retry.steps == 16
    assert retry.handoffs_accepted == 2
    assert retry.handoffs_rejected == 0
    assert [item["failure"] for item in retry.failures] == ["exposure"] * 5
    assert retry.recovery_latencies == [2, 2]
    assert retry.unrecovered_failures == 1
    assert sum(replan.recovery_latencies) < sum(retry.recovery_latencies)
