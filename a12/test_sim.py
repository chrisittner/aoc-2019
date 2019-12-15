from unittest.mock import call, Mock
from .sim import (
    MoonState,
    Position,
    Velocity,
    cycle_length,
    cycle_length_x,
    cycle_length_y,
    cycle_length_z,
    fast_cycle_length,
)


def test_apply_pairwise():
    state = MoonState(
        Position(1, 1, 1), Position(2, 2, 2), Position(3, 3, 3), Position(4, 4, 4)
    )
    f = Mock()
    state.apply_pairwise(f)

    assert f.mock_calls == [
        call(
            {"position": Position(x=1, y=1, z=1), "velocity": Velocity(x=0, y=0, z=0)},
            {"position": Position(x=2, y=2, z=2), "velocity": Velocity(x=0, y=0, z=0)},
        ),
        call(
            {"position": Position(x=1, y=1, z=1), "velocity": Velocity(x=0, y=0, z=0)},
            {"position": Position(x=3, y=3, z=3), "velocity": Velocity(x=0, y=0, z=0)},
        ),
        call(
            {"position": Position(x=1, y=1, z=1), "velocity": Velocity(x=0, y=0, z=0)},
            {"position": Position(x=4, y=4, z=4), "velocity": Velocity(x=0, y=0, z=0)},
        ),
        call(
            {"position": Position(x=2, y=2, z=2), "velocity": Velocity(x=0, y=0, z=0)},
            {"position": Position(x=3, y=3, z=3), "velocity": Velocity(x=0, y=0, z=0)},
        ),
        call(
            {"position": Position(x=2, y=2, z=2), "velocity": Velocity(x=0, y=0, z=0)},
            {"position": Position(x=4, y=4, z=4), "velocity": Velocity(x=0, y=0, z=0)},
        ),
        call(
            {"position": Position(x=3, y=3, z=3), "velocity": Velocity(x=0, y=0, z=0)},
            {"position": Position(x=4, y=4, z=4), "velocity": Velocity(x=0, y=0, z=0)},
        ),
    ]


def test_apply_pairwise_update_state():
    state = MoonState(
        Position(1, 1, 1), Position(2, 2, 2), Position(3, 3, 3), Position(4, 4, 4)
    )

    def increment_x_velocities(moon1, moon2):
        moon1["velocity"].x += 1
        moon2["velocity"].x += 1

    state.apply_pairwise(increment_x_velocities)
    assert [value["velocity"].x for value in state.moons.values()] == [3, 3, 3, 3]


def test_moonstate_steps():
    state = MoonState(
        Position(x=-1, y=0, z=2),
        Position(x=2, y=-10, z=-7),
        Position(x=4, y=-8, z=8),
        Position(x=3, y=5, z=-1),
    )

    state.step()

    assert [(moon["position"], moon["velocity"]) for moon in state.moons.values()] == [
        (Position(x=2, y=-1, z=1), Velocity(x=3, y=-1, z=-1)),
        (Position(x=3, y=-7, z=-4), Velocity(x=1, y=3, z=3)),
        (Position(x=1, y=-7, z=5), Velocity(x=-3, y=1, z=-3)),
        (Position(x=2, y=2, z=0), Velocity(x=-1, y=-3, z=1)),
    ]

    for ii in range(9):
        state.step()

    assert [(moon["position"], moon["velocity"]) for moon in state.moons.values()] == [
        (Position(x=2, y=1, z=-3), Velocity(x=-3, y=-2, z=1)),
        (Position(x=1, y=-8, z=0), Velocity(x=-1, y=1, z=3)),
        (Position(x=3, y=-6, z=1), Velocity(x=3, y=2, z=-3)),
        (Position(x=2, y=0, z=4), Velocity(x=1, y=-1, z=-1)),
    ]

    assert state.total_energy == 179


def test_part1():
    state = MoonState(
        Position(10, 15, 7),
        Position(15, 10, 0),
        Position(20, 12, 3),
        Position(0, -3, 13),
    )
    for ii in range(1000):
        state.step()

    assert state.total_energy == 8362


def test_cycle_length():
    state = MoonState(
        Position(x=-1, y=0, z=2),
        Position(x=2, y=-10, z=-7),
        Position(x=4, y=-8, z=8),
        Position(x=3, y=5, z=-1),
    )

    assert cycle_length(state) == 2772


def test_cycle_length_x():
    state = MoonState(
        Position(x=-1, y=0, z=2),
        Position(x=2, y=-10, z=-7),
        Position(x=4, y=-8, z=8),
        Position(x=3, y=5, z=-1),
    )

    assert cycle_length_x(state) == 18


def test_cycle_length_y():
    state = MoonState(
        Position(x=-1, y=0, z=2),
        Position(x=2, y=-10, z=-7),
        Position(x=4, y=-8, z=8),
        Position(x=3, y=5, z=-1),
    )

    assert cycle_length_y(state) == 28


def test_cycle_length_z():
    state = MoonState(
        Position(x=-1, y=0, z=2),
        Position(x=2, y=-10, z=-7),
        Position(x=4, y=-8, z=8),
        Position(x=3, y=5, z=-1),
    )

    assert cycle_length_z(state) == 44


def test_fast_cycle_length():
    state = MoonState(
        Position(x=-1, y=0, z=2),
        Position(x=2, y=-10, z=-7),
        Position(x=4, y=-8, z=8),
        Position(x=3, y=5, z=-1),
    )

    assert fast_cycle_length(state) == 2772
