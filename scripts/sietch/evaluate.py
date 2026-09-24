"""Registered sandbox scenario v1.

This module reruns the fixed scenario under the replan and retry policies so
the metric definitions can be checked. The numbers describe these scripted
policies in the mock world. They are not measurements of play in any game.
"""

from __future__ import annotations

from pathlib import Path

from sietch.env.mock_world import WorldConfig
from sietch.models import SessionReport
from sietch.orchestrator import run_session

# Frozen with methodology/evaluation.md. Change both together.
REGISTERED_SCENARIO_V1 = {
    "seed": 7,
    "max_steps": 16,
    "water": 4,
    "base_integrity": 3,
    "storm_period": 6,
    "storm_length": 2,
    "max_water": 8,
    "max_base": 10,
}


def scenario_world() -> WorldConfig:
    raw = REGISTERED_SCENARIO_V1
    return WorldConfig(
        seed=int(raw["seed"]),
        water=int(raw["water"]),
        base_integrity=int(raw["base_integrity"]),
        storm_period=int(raw["storm_period"]),
        storm_length=int(raw["storm_length"]),
        max_water=int(raw["max_water"]),
        max_base=int(raw["max_base"]),
    )


def run_registered(style: str, log_path: Path, session_id: str | None = None) -> SessionReport:
    return run_session(
        session_id=session_id or f"scenario-v1-{style}",
        policy_style=style,
        world=scenario_world(),
        max_steps=int(REGISTERED_SCENARIO_V1["max_steps"]),
        operator_present=True,
        human_present=True,
        log_path=log_path,
        clock=lambda: "2026-09-24T00:00:00+00:00",
    )
