"""Sietch sandbox: supervised two-agent research against a mock survival world.

Real-game connection is disabled until written permission exists. This package
does not read game memory, intercept packets, automate input, or touch game files.
"""

from sietch.guard import REAL_GAME_CONNECTION_ENABLED, SANDBOX_ONLY

__version__ = "0.1.0"
__all__ = ["REAL_GAME_CONNECTION_ENABLED", "SANDBOX_ONLY", "__version__"]
