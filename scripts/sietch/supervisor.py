"""Human supervisor: presence check, approval gate, and kill switch.

The operator is a person. This module does not replace that person.
High-impact actions stop at the gate. The default decision is to deny them.
The kill switch ends the loop before the next environment step. It does not
send input to a game, because no game connection exists.
"""

from __future__ import annotations

from collections.abc import Callable

from sietch.logging_jsonl import JsonlLogger
from sietch.models import HIGH_IMPACT_ACTIONS


class OperatorAbsentError(RuntimeError):
    """Raised when a session is asked to start without a human operator."""


class Supervisor:
    def __init__(
        self,
        *,
        human_present: bool,
        approver: Callable[[str], bool] | None = None,
        approval_required: set[str] | None = None,
        before_decision: Callable[["Supervisor"], None] | None = None,
    ) -> None:
        if not human_present:
            raise OperatorAbsentError(
                "A human operator must be present before a session can start. "
                "Pass operator_present and set supervisor.human_present: true."
            )
        self.human_present = True
        self._killed = False
        self.approver = approver or (lambda _action: False)
        self.approval_required = set(approval_required or HIGH_IMPACT_ACTIONS)
        self.before_decision = before_decision
        self.decisions_seen = 0

    @property
    def killed(self) -> bool:
        return self._killed

    def kill(self) -> None:
        """Arm the kill switch. The orchestrator stops before the next step."""
        self._killed = True

    def poll(self) -> bool:
        """Return true when the session must stop. Invokes the test hook first."""
        self.decisions_seen += 1
        if self.before_decision is not None:
            self.before_decision(self)
        return self._killed

    def review(self, action: str, logger: JsonlLogger | None = None) -> bool:
        """Return true when the action may be applied.

        Ordinary actions pass. High-impact actions are logged and sent to the
        approver. A missing approver denies them.
        """
        if action not in self.approval_required:
            return True
        if logger is not None:
            logger.write("approval_requested", action=action, gate="human")
        granted = bool(self.approver(action))
        if logger is not None:
            logger.write(
                "approval_granted" if granted else "approval_denied",
                action=action,
                granted=granted,
            )
        return granted
