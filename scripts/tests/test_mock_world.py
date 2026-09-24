"""Direct checks of the mock world's failure and recovery transitions."""

from __future__ import annotations

from sietch.env.mock_world import MockSurvivalWorld, WorldConfig


def test_same_seed_is_deterministic() -> None:
    first = MockSurvivalWorld(WorldConfig())
    second = MockSurvivalWorld(WorldConfig())
    actions = ["scout", "gather_water", "rest", "enter_shelter", "repair_base"]
    for action in actions:
        assert first.step(action).snapshot() == second.step(action).snapshot()


def test_gather_during_storm_is_exposure() -> None:
    world = MockSurvivalWorld(WorldConfig(storm_period=6, storm_length=2))
    world.reset()
    # Steps land on ticks 1, 2, 3, 4. Tick 4 is inside the storm window.
    for _ in range(3):
        world.step("rest")
    caught = world.step("gather_water")
    assert caught.tick == 4
    assert caught.storm is True
    assert caught.failure == "exposure"


def test_shelter_then_gather_during_storm_succeeds() -> None:
    world = MockSurvivalWorld(WorldConfig(water=8))
    world.reset()
    for _ in range(3):
        world.step("rest")
    sheltered = world.step("enter_shelter")
    assert sheltered.tick == 4
    assert sheltered.sheltered is True
    assert sheltered.failure is None
    gathered = world.step("gather_water")
    assert gathered.storm is True
    assert gathered.failure is None
    assert gathered.water > 0


def test_discard_water_is_not_a_normal_failure_mode() -> None:
    world = MockSurvivalWorld(WorldConfig(water=5))
    world.reset()
    obs = world.step("discard_water")
    assert obs.water == 0
    assert obs.failure == "water_discarded"


def test_unknown_action_is_a_failure() -> None:
    world = MockSurvivalWorld(WorldConfig())
    world.reset()
    obs = world.step("fly")
    assert obs.failure == "unknown_action"
