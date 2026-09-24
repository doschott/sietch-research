"""Shared records for observations, handoffs, and session reports."""

from __future__ import annotations

from dataclasses import dataclass, field

ENV_ACTIONS = frozenset(
    {
        "gather_water",
        "enter_shelter",
        "leave_shelter",
        "repair_base",
        "scout",
        "rest",
        "abandon_shelter",
        "discard_water",
    }
)

HIGH_IMPACT_ACTIONS = frozenset({"abandon_shelter", "discard_water"})

SNAPSHOT_KEYS = (
    "tick",
    "water",
    "sheltered",
    "storm",
    "base_integrity",
    "failure",
)


@dataclass(frozen=True)
class Observation:
    tick: int
    water: int
    sheltered: bool
    storm: bool
    storm_in: int | None
    base_integrity: int
    shelter_locked: int
    failure: str | None
    failures: tuple[str, ...] = ()

    def snapshot(self) -> dict[str, object]:
        return {
            "tick": self.tick,
            "water": self.water,
            "sheltered": self.sheltered,
            "storm": self.storm,
            "storm_in": self.storm_in,
            "base_integrity": self.base_integrity,
            "shelter_locked": self.shelter_locked,
            "failure": self.failure,
            "failures": list(self.failures),
        }


@dataclass(frozen=True)
class HandoffRecord:
    """Information one agent must pass before the other may take the task.

    A record is complete only when every field the orchestrator requires is present.
    Empty lists are allowed. Missing lists are not.
    """

    from_agent: str
    to_agent: str
    goal: str
    reason: str
    world_snapshot: dict[str, object] | None
    open_commitments: list[str] | None
    failure_history: list[str] | None

    def missing_fields(self) -> list[str]:
        missing: list[str] = []
        if not self.from_agent:
            missing.append("from_agent")
        if not self.to_agent:
            missing.append("to_agent")
        if self.from_agent and self.to_agent and self.from_agent == self.to_agent:
            missing.append("to_agent")
        if not self.goal:
            missing.append("goal")
        if not self.reason:
            missing.append("reason")
        if not isinstance(self.world_snapshot, dict):
            missing.append("world_snapshot")
        else:
            for key in SNAPSHOT_KEYS:
                if key not in self.world_snapshot:
                    missing.append(f"world_snapshot.{key}")
        if not isinstance(self.open_commitments, list):
            missing.append("open_commitments")
        if not isinstance(self.failure_history, list):
            missing.append("failure_history")
        return missing


@dataclass
class Assignment:
    owner: str
    goal: str
    open_commitments: list[str] = field(default_factory=list)
    failure_history: list[str] = field(default_factory=list)

    def apply(self, record: HandoffRecord) -> None:
        self.owner = record.to_agent
        self.goal = record.goal
        self.open_commitments = list(record.open_commitments or [])
        self.failure_history = list(record.failure_history or [])


@dataclass(frozen=True)
class Decision:
    kind: str
    action: str | None = None
    handoff: HandoffRecord | None = None


@dataclass
class SessionReport:
    session_id: str
    policy_style: str
    steps: int
    handoffs_accepted: int
    handoffs_rejected: int
    failures: list[dict[str, object]]
    recovery_latencies: list[int]
    unrecovered_failures: int
    approval_blocks: int
    killed: bool
    final_water: int
    final_base: int
    final_owner: str
    final_goal: str

    def summary(self) -> str:
        latencies = ", ".join(str(item) for item in self.recovery_latencies) or "none"
        return (
            f"session {self.session_id} style={self.policy_style} "
            f"steps={self.steps} handoffs_accepted={self.handoffs_accepted} "
            f"handoffs_rejected={self.handoffs_rejected} "
            f"failures={len(self.failures)} recovery_latencies=[{latencies}] "
            f"unrecovered={self.unrecovered_failures} "
            f"approval_blocks={self.approval_blocks} killed={self.killed} "
            f"water={self.final_water} base={self.final_base} "
            f"owner={self.final_owner} goal={self.final_goal}"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "policy_style": self.policy_style,
            "steps": self.steps,
            "handoffs_accepted": self.handoffs_accepted,
            "handoffs_rejected": self.handoffs_rejected,
            "failures": self.failures,
            "recovery_latencies": self.recovery_latencies,
            "unrecovered_failures": self.unrecovered_failures,
            "approval_blocks": self.approval_blocks,
            "killed": self.killed,
            "final_water": self.final_water,
            "final_base": self.final_base,
            "final_owner": self.final_owner,
            "final_goal": self.final_goal,
        }
