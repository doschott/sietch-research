"""Deterministic mock survival world.

The world tracks water, shelter, storms, and base integrity. It is an abstract
instrument for planning, handoff, and failure recovery. It is not a model of
any commercial game, and it does not load game files.

Storms follow the seed only through the configured period and length, so two
runs with the same WorldConfig produce the same episode.
"""

from __future__ import annotations

from dataclasses import dataclass

from sietch.env.interface import Environment
from sietch.guard import assert_sandbox_only
from sietch.models import ENV_ACTIONS, Observation


@dataclass(frozen=True)
class WorldConfig:
    seed: int = 7
    water: int = 4
    base_integrity: int = 3
    storm_period: int = 6
    storm_length: int = 2
    max_water: int = 8
    max_base: int = 10

    def __post_init__(self) -> None:
        if self.storm_period < 2:
            raise ValueError("storm_period must be at least 2")
        if not 1 <= self.storm_length < self.storm_period:
            raise ValueError("storm_length must be at least 1 and shorter than storm_period")
        if self.water < 0 or self.base_integrity < 0:
            raise ValueError("water and base_integrity must be non-negative")
        if self.max_water < 1 or self.max_base < 1:
            raise ValueError("caps must be positive")


class MockSurvivalWorld(Environment):
    """In-process survival world with partial storm forecasts."""

    def __init__(self, config: WorldConfig | None = None) -> None:
        self.config = config or WorldConfig()
        self.tick = 0
        self.water = self.config.water
        self.base_integrity = self.config.base_integrity
        self.sheltered = False
        self.shelter_locked = 0
        self.forecast_until = -1
        self.failure: str | None = None
        self.failures: tuple[str, ...] = ()

    def reset(self) -> Observation:
        self.tick = 0
        self.water = self.config.water
        self.base_integrity = self.config.base_integrity
        self.sheltered = False
        self.shelter_locked = 0
        self.forecast_until = -1
        self.failure = None
        self.failures = ()
        return self.observe()

    def observe(self) -> Observation:
        return Observation(
            tick=self.tick,
            water=self.water,
            sheltered=self.sheltered,
            storm=self.storm_at(self.tick),
            storm_in=self._storm_in(),
            base_integrity=self.base_integrity,
            shelter_locked=self.shelter_locked,
            failure=self.failure,
            failures=self.failures,
        )

    def available_actions(self) -> tuple[str, ...]:
        return tuple(sorted(ENV_ACTIONS))

    def step(self, action: str) -> Observation:
        if action not in ENV_ACTIONS:
            self.tick += 1
            self._metabolize()
            self._set_failures(["unknown_action"])
            return self.observe()

        self.tick += 1
        if self.shelter_locked > 0:
            self.shelter_locked -= 1
            self.sheltered = False

        storm = self.storm_at(self.tick)
        exposed = storm and not self.sheltered
        action_failure: str | None = None
        skip_metabolism = False

        if action == "gather_water":
            if exposed:
                action_failure = "exposure"
            else:
                self.water = min(self.config.max_water, self.water + 2)
        elif action == "enter_shelter":
            if self.shelter_locked > 0:
                action_failure = "shelter_unavailable"
            else:
                self.sheltered = True
        elif action == "leave_shelter":
            self.sheltered = False
            if storm:
                action_failure = "exposure"
        elif action == "repair_base":
            if exposed:
                action_failure = "exposure"
            elif self.water < 1:
                action_failure = "insufficient_water"
            else:
                self.water -= 1
                self.base_integrity = min(self.config.max_base, self.base_integrity + 2)
        elif action == "scout":
            if exposed:
                action_failure = "exposure"
            else:
                self.forecast_until = self.tick + self.config.storm_period
        elif action == "rest":
            if exposed:
                action_failure = "exposure"
        elif action == "abandon_shelter":
            self.shelter_locked = 5
            self.sheltered = False
            action_failure = "shelter_abandoned"
        elif action == "discard_water":
            self.water = 0
            action_failure = "water_discarded"
            skip_metabolism = True

        if not skip_metabolism:
            self._metabolize()

        failures: list[str] = []
        if action_failure:
            failures.append(action_failure)
        if self.water == 0 and "dehydration" not in failures and action_failure != "water_discarded":
            failures.append("dehydration")
        self._set_failures(failures)
        return self.observe()

    def storm_at(self, tick: int) -> bool:
        position = tick % self.config.storm_period
        return position >= (self.config.storm_period - self.config.storm_length)

    def _storm_in(self) -> int | None:
        if self.tick > self.forecast_until:
            return None
        for ahead in range(0, self.config.storm_period + 1):
            if self.storm_at(self.tick + ahead):
                return ahead
        return None

    def _metabolize(self) -> None:
        self.water = max(0, self.water - 1)

    def _set_failures(self, failures: list[str]) -> None:
        self.failures = tuple(failures)
        self.failure = failures[0] if failures else None


def open_environment(mode: str, config: WorldConfig | None = None) -> MockSurvivalWorld:
    """Open the mock world. Any other mode raises RealGameConnectionDisabled."""
    assert_sandbox_only(mode)
    return MockSurvivalWorld(config)
