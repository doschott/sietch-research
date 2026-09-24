"""Agent policies.

The default policy is a deterministic script. It runs offline.
LLMPolicy is a plug for a caller-supplied client. Constructing it does not
open a network connection. Choosing an action without a client raises.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Protocol

from sietch.models import ENV_ACTIONS, Assignment, Decision, HandoffRecord, Observation


class LanguageModelClient(Protocol):
    def complete(self, messages: list[dict[str, str]]) -> str:
        """Return a model completion. Implementations are injected by the caller."""


class LLMClientNotConfigured(RuntimeError):
    """Raised when an LLM policy is asked to act without an injected client."""


class ScriptedPolicy:
    """Baseline policy for Eve (planner) and Edos (recovery).

    style='replan' hands a failed task to the other agent with a full record.
    style='retry' repeats the previous environment action up to max_repeats
    times before falling through to the same planner rules.

    The planner gathers when water is at or below 2, including during a storm.
    That brittleness is intentional: the registered scenario needs a failure
    the recovery rules can answer. The forecast from scout is recorded and
    then ignored by this baseline.
    """

    def __init__(
        self,
        style: str = "replan",
        handoff_style: str = "complete",
        max_repeats: int = 4,
        force_action: str | None = None,
    ) -> None:
        if style not in {"replan", "retry"}:
            raise ValueError("style must be 'replan' or 'retry'")
        if handoff_style not in {"complete", "minimal"}:
            raise ValueError("handoff_style must be 'complete' or 'minimal'")
        self.style = style
        self.handoff_style = handoff_style
        self.max_repeats = max_repeats
        self.force_action = force_action
        self._used_force = False
        self._last_action: str | None = None
        self._repeats = 0

    def choose(self, agent_id: str, obs: Observation, assignment: Assignment) -> Decision:
        if self.force_action and not self._used_force:
            self._used_force = True
            self._last_action = self.force_action
            return Decision(kind="act", action=self.force_action)

        if (
            obs.failure
            and self.style == "retry"
            and self._last_action
            and self._repeats < self.max_repeats
        ):
            self._repeats += 1
            return Decision(kind="act", action=self._last_action)

        self._repeats = 0
        if agent_id == "edos":
            decision = self._edos(obs, assignment)
        else:
            decision = self._eve(obs, assignment)
        if decision.kind == "act" and decision.action:
            self._last_action = decision.action
        return decision

    def _eve(self, obs: Observation, assignment: Assignment) -> Decision:
        if obs.failure and self.style == "replan":
            return self._handoff(
                "eve",
                "edos",
                "recover",
                obs.failure,
                obs,
                assignment,
                [f"clear failure:{obs.failure}", "restore water above 2"],
            )
        if assignment.goal == "refill" or obs.water <= 2:
            return Decision(kind="act", action="gather_water")
        if obs.storm and not obs.sheltered:
            return Decision(kind="act", action="enter_shelter")
        if obs.base_integrity <= 4 and obs.water >= 4:
            return self._handoff(
                "eve",
                "edos",
                "repair_base",
                "base integrity is low",
                obs,
                assignment,
                ["raise base integrity to at least 6"],
            )
        if obs.storm_in is None:
            return Decision(kind="act", action="scout")
        return Decision(kind="act", action="rest")

    def _edos(self, obs: Observation, assignment: Assignment) -> Decision:
        goal = assignment.goal
        if goal == "repair_base":
            if obs.storm and not obs.sheltered:
                return Decision(kind="act", action="enter_shelter")
            if obs.water < 3:
                return self._handoff(
                    "edos",
                    "eve",
                    "refill",
                    "water is too low to repair",
                    obs,
                    assignment,
                    ["raise water above 2"],
                )
            if obs.base_integrity >= 6:
                return self._handoff(
                    "edos",
                    "eve",
                    "maintain",
                    "repair target met",
                    obs,
                    assignment,
                    ["keep water above 2"],
                )
            return Decision(kind="act", action="repair_base")
        if goal == "recover":
            if obs.storm and not obs.sheltered:
                return Decision(kind="act", action="enter_shelter")
            if obs.water <= 2:
                return Decision(kind="act", action="gather_water")
            return self._handoff(
                "edos",
                "eve",
                "maintain",
                "recovered",
                obs,
                assignment,
                ["keep water above 2"],
            )
        if goal == "hold_shelter":
            if not obs.sheltered:
                return Decision(kind="act", action="enter_shelter")
            if obs.storm:
                return Decision(kind="act", action="rest")
            return self._handoff(
                "edos",
                "eve",
                "maintain",
                "storm passed",
                obs,
                assignment,
                ["keep water above 2"],
            )
        return Decision(kind="act", action="rest")

    def _handoff(
        self,
        sender: str,
        receiver: str,
        goal: str,
        reason: str,
        obs: Observation,
        assignment: Assignment,
        commitments: list[str],
    ) -> Decision:
        history = list(assignment.failure_history)
        if obs.failure and obs.failure not in history:
            history.append(obs.failure)
        if self.handoff_style == "minimal":
            record = HandoffRecord(
                from_agent=sender,
                to_agent=receiver,
                goal=goal,
                reason="",
                world_snapshot=None,
                open_commitments=None,
                failure_history=None,
            )
        else:
            record = HandoffRecord(
                from_agent=sender,
                to_agent=receiver,
                goal=goal,
                reason=reason,
                world_snapshot=obs.snapshot(),
                open_commitments=list(commitments),
                failure_history=history,
            )
        return Decision(kind="handoff", handoff=record)


class LLMPolicy:
    """Optional policy. The client is injected. The default session never builds one."""

    def __init__(self, client: LanguageModelClient | None = None) -> None:
        self.client = client

    def choose(self, agent_id: str, obs: Observation, assignment: Assignment) -> Decision:
        if self.client is None:
            raise LLMClientNotConfigured(
                "No language-model client is configured. The default run is offline "
                "and uses ScriptedPolicy. Inject a client in process if you need this "
                "plug. This class does not open a network connection by itself."
            )
        raw = self.client.complete(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a sandbox agent. Reply with a JSON object "
                        '{"action": "<name>"} and no other text. '
                        f"Allowed actions: {', '.join(sorted(ENV_ACTIONS))}."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "agent": agent_id,
                            "goal": assignment.goal,
                            "observation": obs.snapshot(),
                        }
                    ),
                },
            ]
        )
        data = json.loads(raw)
        if not isinstance(data, Mapping) or "action" not in data:
            raise ValueError("Language-model policy must return a JSON object with 'action'")
        action = str(data["action"])
        if action not in ENV_ACTIONS:
            raise ValueError(f"Language-model policy returned an unknown action: {action}")
        return Decision(kind="act", action=action)
