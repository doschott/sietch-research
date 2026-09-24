"""Load sandbox YAML. A config that asks for a live game is rejected."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from sietch.env.mock_world import WorldConfig
from sietch.guard import RealGameConnectionDisabled, assert_sandbox_only
from sietch.models import HIGH_IMPACT_ACTIONS


@dataclass(frozen=True)
class SessionConfig:
    mode: str
    real_game_connection: bool
    policy_style: str
    policy_name: str
    max_steps: int
    session_id: str | None
    human_present: bool
    log_path: Path
    world: WorldConfig
    approval_required: set[str]


def load_config(path: Path) -> SessionConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Config root must be a mapping")
    mode = str(raw.get("mode", ""))
    real_game = bool(raw.get("real_game_connection", False))
    try:
        assert_sandbox_only(mode)
    except RealGameConnectionDisabled as exc:
        raise RealGameConnectionDisabled(str(exc)) from exc
    if real_game:
        raise RealGameConnectionDisabled(
            "real_game_connection must be false. "
            "This repository has no game connector, and the flag cannot enable one."
        )
    world_raw = raw.get("world") or {}
    if not isinstance(world_raw, dict):
        raise ValueError("world must be a mapping")
    world = WorldConfig(
        seed=int(raw.get("seed", 7)),
        water=int(world_raw.get("water", 4)),
        base_integrity=int(world_raw.get("base_integrity", 3)),
        storm_period=int(world_raw.get("storm_period", 6)),
        storm_length=int(world_raw.get("storm_length", 2)),
        max_water=int(world_raw.get("max_water", 8)),
        max_base=int(world_raw.get("max_base", 10)),
    )
    supervisor = raw.get("supervisor") or {}
    logging_raw = raw.get("logging") or {}
    if not isinstance(supervisor, dict) or not isinstance(logging_raw, dict):
        raise ValueError("supervisor and logging must be mappings")
    policy_style = str(raw.get("policy_style", "replan"))
    if policy_style not in {"replan", "retry"}:
        raise ValueError("policy_style must be 'replan' or 'retry'")
    policy_name = str(raw.get("policy", "scripted"))
    if policy_name not in {"scripted", "llm"}:
        raise ValueError("policy must be 'scripted' or 'llm'")
    approval = supervisor.get("approval_required", sorted(HIGH_IMPACT_ACTIONS))
    if not isinstance(approval, list) or not all(isinstance(item, str) for item in approval):
        raise ValueError("approval_required must be a list of strings")
    log_path = Path(str(logging_raw.get("path", "sessions/sandbox.jsonl")))
    session_id = raw.get("session_id")
    return SessionConfig(
        mode=mode,
        real_game_connection=False,
        policy_style=policy_style,
        policy_name=policy_name,
        max_steps=int(raw.get("max_steps", 16)),
        session_id=None if session_id in (None, "null") else str(session_id),
        human_present=bool(supervisor.get("human_present", False)),
        log_path=log_path,
        world=world,
        approval_required=set(approval),
    )
