"""Two-agent loop with handoff, approval, logging, and a kill switch.

Handoffs do not advance the world clock. At most one handoff is accepted on a
given observation. A rejected handoff is followed by a rest step so the loop
cannot spin. High-impact actions that the operator denies are replaced with rest
and are not applied.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from sietch.env.mock_world import MockSurvivalWorld, WorldConfig, open_environment
from sietch.guard import RealGameConnectionDisabled, assert_sandbox_only
from sietch.logging_jsonl import JsonlLogger
from sietch.models import HIGH_IMPACT_ACTIONS, Assignment, SessionReport
from sietch.policies import ScriptedPolicy
from sietch.supervisor import OperatorAbsentError, Supervisor


def run_session(
    *,
    session_id: str,
    policy_style: str = "replan",
    world: WorldConfig | None = None,
    max_steps: int = 16,
    operator_present: bool = False,
    human_present: bool = True,
    log_path: Path,
    approver: Callable[[str], bool] | None = None,
    approval_required: set[str] | None = None,
    clock: Callable[[], str] | None = None,
    policies: dict[str, object] | None = None,
    before_decision: Callable[[Supervisor], None] | None = None,
    mode: str = "sandbox",
    real_game_connection: bool = False,
) -> SessionReport:
    """Run one supervised sandbox session and return its report."""
    assert_sandbox_only(mode)
    if real_game_connection:
        raise RealGameConnectionDisabled(
            "Config asked for a real-game connection. That setting is refused."
        )
    if not operator_present or not human_present:
        raise OperatorAbsentError(
            "A human operator must be present for every session. "
            "The config flag and the caller flag both have to be true."
        )

    supervisor = Supervisor(
        human_present=True,
        approver=approver,
        approval_required=approval_required or set(HIGH_IMPACT_ACTIONS),
        before_decision=before_decision,
    )
    env: MockSurvivalWorld = open_environment("sandbox", world)
    obs = env.reset()
    logger = JsonlLogger(log_path, session_id, clock=clock)
    logger.write(
        "session_start",
        mode="sandbox",
        policy_style=policy_style,
        seed=env.config.seed,
        max_steps=max_steps,
        agents=["eve", "edos"],
        operator_role="human_operator",
        real_game_connection=False,
    )

    if policies is None:
        policies = {
            "eve": ScriptedPolicy(style=policy_style),
            "edos": ScriptedPolicy(style=policy_style),
        }
    assignment = Assignment(owner="eve", goal="maintain")
    handoffs_on_obs = 0
    accepted = 0
    rejected = 0
    blocks = 0
    failures: list[dict[str, object]] = []
    latencies: list[int] = []
    open_failure_tick: int | None = None
    steps = 0
    killed = False

    def track(observation_failure: str | None, tick: int) -> None:
        nonlocal open_failure_tick
        if observation_failure and open_failure_tick is None:
            open_failure_tick = tick
        elif observation_failure is None and open_failure_tick is not None:
            latencies.append(tick - open_failure_tick)
            open_failure_tick = None

    while steps < max_steps:
        if supervisor.poll():
            killed = True
            logger.write("kill_switch", reason="operator", steps=steps)
            break

        agent_id = assignment.owner
        policy = policies[agent_id]
        decision = policy.choose(agent_id, obs, assignment)  # type: ignore[attr-defined]
        if decision.kind == "handoff":
            record = decision.handoff
            missing = [] if record is None else record.missing_fields()
            if record is None:
                missing = ["handoff"]
            logger.write(
                "decision",
                agent=agent_id,
                kind="handoff",
                goal=None if record is None else record.goal,
                missing=missing,
            )
            if missing or handoffs_on_obs >= 1:
                reason = missing or ["churn"]
                logger.write("handoff_rejected", agent=agent_id, missing=reason)
                rejected += 1
                obs = _apply(env, "rest", agent_id, logger)
                steps += 1
                handoffs_on_obs = 0
                if obs.failure:
                    failures.append({"tick": obs.tick, "failure": obs.failure, "agent": agent_id})
                track(obs.failure, obs.tick)
                continue
            assert record is not None
            assignment.apply(record)
            handoffs_on_obs += 1
            accepted += 1
            logger.write(
                "handoff_accepted",
                from_agent=record.from_agent,
                to_agent=record.to_agent,
                goal=record.goal,
                reason=record.reason,
                open_commitments=record.open_commitments,
                failure_history=record.failure_history,
            )
            continue

        action = decision.action or "rest"
        logger.write("decision", agent=agent_id, kind="act", action=action)
        if action in supervisor.approval_required:
            if not supervisor.review(action, logger):
                blocks += 1
                logger.write("substituted_rest", agent=agent_id, blocked_action=action)
                action = "rest"
        if supervisor.killed:
            killed = True
            logger.write("kill_switch", reason="operator", steps=steps)
            break
        obs = _apply(env, action, agent_id, logger)
        steps += 1
        handoffs_on_obs = 0
        if obs.failure:
            failures.append(
                {
                    "tick": obs.tick,
                    "failure": obs.failure,
                    "failures": list(obs.failures),
                    "agent": agent_id,
                    "action": action,
                }
            )
        track(obs.failure, obs.tick)

    unrecovered = 1 if open_failure_tick is not None else 0
    report = SessionReport(
        session_id=session_id,
        policy_style=policy_style,
        steps=steps,
        handoffs_accepted=accepted,
        handoffs_rejected=rejected,
        failures=failures,
        recovery_latencies=latencies,
        unrecovered_failures=unrecovered,
        approval_blocks=blocks,
        killed=killed,
        final_water=obs.water,
        final_base=obs.base_integrity,
        final_owner=assignment.owner,
        final_goal=assignment.goal,
    )
    logger.write("session_end", **report.to_dict())
    return report


def _apply(env: MockSurvivalWorld, action: str, agent: str, logger: JsonlLogger):
    obs = env.step(action)
    logger.write(
        "action_result",
        agent=agent,
        action=action,
        tick=obs.tick,
        water=obs.water,
        sheltered=obs.sheltered,
        storm=obs.storm,
        base_integrity=obs.base_integrity,
        failure=obs.failure,
        failures=list(obs.failures),
    )
    return obs
