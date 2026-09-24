"""The package must refuse every real-game path."""

from __future__ import annotations

import pytest

from sietch import guard
from sietch.env.mock_world import open_environment
from sietch.guard import (
    REAL_GAME_CONNECTION_ENABLED,
    RealGameConnectionDisabled,
    assert_sandbox_only,
    connect_real_game,
)


def test_flag_ships_disabled() -> None:
    assert REAL_GAME_CONNECTION_ENABLED is False
    assert guard.SANDBOX_ONLY is True


def test_sandbox_mode_opens_mock() -> None:
    world = open_environment("sandbox")
    obs = world.reset()
    assert obs.tick == 0
    assert "gather_water" in world.available_actions()


@pytest.mark.parametrize("mode", ["game", "dune", "awakening", "client", ""])
def test_named_modes_are_refused(mode: str) -> None:
    with pytest.raises(RealGameConnectionDisabled):
        open_environment(mode)


def test_connect_real_game_is_refused() -> None:
    with pytest.raises(RealGameConnectionDisabled):
        connect_real_game(host="127.0.0.1")


def test_flipping_the_flag_still_refuses(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(guard, "REAL_GAME_CONNECTION_ENABLED", True)
    with pytest.raises(RealGameConnectionDisabled):
        assert_sandbox_only("sandbox")
