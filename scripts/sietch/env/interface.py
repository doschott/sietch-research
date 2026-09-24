"""Abstract environment API for a survival-world sandbox.

Implementations must be in-process simulations. A class that talks to a game
client does not belong behind this interface. See sietch.guard.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sietch.models import Observation


class Environment(ABC):
    """Minimal world API used by the orchestrator."""

    @abstractmethod
    def reset(self) -> Observation:
        """Return the world to its configured initial state."""

    @abstractmethod
    def observe(self) -> Observation:
        """Return the current observation without changing the world."""

    @abstractmethod
    def step(self, action: str) -> Observation:
        """Apply one environment action and return the next observation."""

    @abstractmethod
    def available_actions(self) -> tuple[str, ...]:
        """Names the orchestrator is allowed to send to step()."""
