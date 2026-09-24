"""Safety guard for the environment boundary.

The only environment this package can open is the in-process mock survival world.
There is no connector to a game client. The flag below stays false on purpose:
flipping it does not enable a connection, and every open path still refuses.
"""

from __future__ import annotations

SANDBOX_ONLY = True
REAL_GAME_CONNECTION_ENABLED = False

SANDBOX_MODE = "sandbox"


class RealGameConnectionDisabled(RuntimeError):
    """Raised when code asks for anything other than the mock sandbox."""


_DISABLED_MESSAGE = (
    "Real-game connection is disabled until written permission exists. "
    "This package can open the mock survival-world sandbox only. "
    "It does not read game memory, intercept packets, automate input into a game, "
    "or touch Dune: Awakening files. If permission is later granted with conditions, "
    "those conditions have to be implemented in a reviewed change. "
    "Setting REAL_GAME_CONNECTION_ENABLED to true does not create a connector."
)


def assert_sandbox_only(mode: str) -> None:
    """Refuse every mode except the mock sandbox, including a flipped flag."""
    if mode != SANDBOX_MODE or REAL_GAME_CONNECTION_ENABLED:
        raise RealGameConnectionDisabled(_DISABLED_MESSAGE)


def connect_real_game(*_args: object, **_kwargs: object) -> None:
    """Public refusal point. A future connector must not be added behind this name."""
    raise RealGameConnectionDisabled(_DISABLED_MESSAGE)
