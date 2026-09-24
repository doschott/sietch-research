"""Command-line entry for one offline sandbox session.

The process refuses to start unless the caller passes --operator-present and
the config also sets supervisor.human_present. SIGINT arms the kill switch.
The language-model policy is not available from this command.
"""

from __future__ import annotations

import argparse
import signal
import sys
import uuid
from pathlib import Path

from sietch.config import load_config
from sietch.guard import RealGameConnectionDisabled
from sietch.orchestrator import run_session
from sietch.supervisor import OperatorAbsentError, Supervisor


def run_from_config(
    path: Path,
    *,
    operator_present: bool,
    steps: int | None = None,
    log_path: Path | None = None,
    seed: int | None = None,
    before_decision=None,
):
    config = load_config(path)
    if config.policy_name == "llm":
        raise RuntimeError(
            "The command-line runner uses the scripted policy only. "
            "LLMPolicy can be constructed in code with an injected client. "
            "This command does not contact a model provider."
        )
    world = config.world
    if seed is not None:
        from sietch.env.mock_world import WorldConfig

        world = WorldConfig(
            seed=seed,
            water=world.water,
            base_integrity=world.base_integrity,
            storm_period=world.storm_period,
            storm_length=world.storm_length,
            max_water=world.max_water,
            max_base=world.max_base,
        )
    session_id = config.session_id or f"sandbox-{uuid.uuid4().hex[:8]}"
    return run_session(
        session_id=session_id,
        policy_style=config.policy_style,
        world=world,
        max_steps=config.max_steps if steps is None else steps,
        operator_present=operator_present,
        human_present=config.human_present,
        log_path=log_path or config.log_path,
        approval_required=config.approval_required,
        before_decision=before_decision,
        mode=config.mode,
        real_game_connection=config.real_game_connection,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run Eve and Edos in the mock survival sandbox. "
            "Real-game connection is disabled."
        )
    )
    parser.add_argument("--config", required=True, help="Path to a sandbox YAML file")
    parser.add_argument(
        "--operator-present",
        action="store_true",
        help="Confirm that a human operator is present for this session",
    )
    parser.add_argument("--steps", type=int, default=None, help="Override max_steps")
    parser.add_argument("--log", default=None, help="Override the JSONL log path")
    parser.add_argument("--seed", type=int, default=None, help="Override the world seed")
    args = parser.parse_args(argv)

    holder: dict[str, Supervisor] = {}

    def before_decision(supervisor: Supervisor) -> None:
        holder["supervisor"] = supervisor

    def on_sigint(_signum: int, _frame: object) -> None:
        supervisor = holder.get("supervisor")
        if supervisor is not None:
            supervisor.kill()
        else:
            raise KeyboardInterrupt

    previous = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, on_sigint)
    try:
        report = run_from_config(
            Path(args.config),
            operator_present=args.operator_present,
            steps=args.steps,
            log_path=None if args.log is None else Path(args.log),
            seed=args.seed,
            before_decision=before_decision,
        )
    except OperatorAbsentError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (RealGameConnectionDisabled, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 3
    finally:
        signal.signal(signal.SIGINT, previous)
    print(report.summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
