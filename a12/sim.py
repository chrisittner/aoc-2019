from collections import namedtuple
from itertools import combinations
from dataclasses import dataclass


def sign(value: int):
    if value == 0:
        return 0
    if value <= 0:
        return -1
    return 1


@dataclass
class Position:
    x: int
    y: int
    z: int


@dataclass
class Velocity:
    x: int
    y: int
    z: int


class MoonState:
    def __init__(
        self, io: Position, europa: Position, ganymede: Position, callisto: Position
    ):
        self.time = 0
        self.moons = {
            "Io": {"position": io, "velocity": Velocity(0, 0, 0)},
            "Europa": {"position": europa, "velocity": Velocity(0, 0, 0)},
            "Ganymede": {"position": ganymede, "velocity": Velocity(0, 0, 0)},
            "Callisto": {"position": callisto, "velocity": Velocity(0, 0, 0)},
        }

    def apply_pairwise(self, f):
        """applies f(moon1, moon2) to all pairs of moons"""
        pairs = combinations(self.moons.values(), 2)
        for pair in pairs:
            f(*pair)

    def step(self):
        self.apply_pairwise(self.step_gravity)
        for moon in self.moons.values():
            self.step_velocity(moon)

        self.time += 1

    @property
    def total_energy(self):
        return sum(
            [
                self.kinetic_energy(moon) * self.potential_energy(moon)
                for moon in self.moons.values()
            ]
        )

    @staticmethod
    def potential_energy(moon):
        return sum(
            [
                abs(val)
                for val in (moon["position"].x, moon["position"].y, moon["position"].z,)
            ]
        )

    @staticmethod
    def kinetic_energy(moon):
        return sum(
            [
                abs(val)
                for val in (moon["velocity"].x, moon["velocity"].y, moon["velocity"].z,)
            ]
        )

    @staticmethod
    def step_gravity(moon1, moon2):
        p1 = moon1["position"]
        v1 = moon1["velocity"]
        p2 = moon2["position"]
        v2 = moon2["velocity"]

        v1.x += sign(p2.x - p1.x)
        v1.y += sign(p2.y - p1.y)
        v1.z += sign(p2.z - p1.z)
        v2.x += sign(p1.x - p2.x)
        v2.y += sign(p1.y - p2.y)
        v2.z += sign(p1.z - p2.z)

    @staticmethod
    def step_velocity(moon):
        moon["position"].x += moon["velocity"].x
        moon["position"].y += moon["velocity"].y
        moon["position"].z += moon["velocity"].z


def cycle_length(state: MoonState) -> int:
    target_state = [
        (
            (moon["position"].x, moon["position"].y, moon["position"].z),
            (moon["velocity"].x, moon["velocity"].y, moon["velocity"].z),
        )
        for moon in state.moons.values()
    ]
    state.time = 0
    state.step()

    while (
        not [
            (
                (moon["position"].x, moon["position"].y, moon["position"].z),
                (moon["velocity"].x, moon["velocity"].y, moon["velocity"].z),
            )
            for moon in state.moons.values()
        ]
        == target_state
    ):
        state.step()
        # print(state.total_energy)

    return state.time


def cycle_length_x(state: MoonState) -> int:
    target_state = [
        (moon["position"].x, moon["velocity"].x,) for moon in state.moons.values()
    ]
    state.time = 0
    state.step()

    while (
        not [(moon["position"].x, moon["velocity"].x,) for moon in state.moons.values()]
        == target_state
    ):
        state.step()

    return state.time


def cycle_length_y(state: MoonState) -> int:
    target_state = [
        (moon["position"].y, moon["velocity"].y,) for moon in state.moons.values()
    ]
    state.time = 0
    state.step()

    while (
        not [(moon["position"].y, moon["velocity"].y,) for moon in state.moons.values()]
        == target_state
    ):
        state.step()

    return state.time


def cycle_length_z(state: MoonState) -> int:
    target_state = [
        (moon["position"].z, moon["velocity"].z,) for moon in state.moons.values()
    ]
    state.time = 0
    state.step()

    while (
        not [(moon["position"].z, moon["velocity"].z,) for moon in state.moons.values()]
        == target_state
    ):
        state.step()

    return state.time


def fast_cycle_length(state: MoonState):
    from copy import deepcopy
    from math import gcd

    x = cycle_length_x(deepcopy(state))
    y = cycle_length_y(deepcopy(state))
    z = cycle_length_z(deepcopy(state))

    lcm_xy = x * y // gcd(x, y)
    lcm = lcm_xy * z // gcd(lcm_xy, z)

    return lcm  # = np.lcm.reduce([x,y,z])


if __name__ == "__main__":
    state = MoonState(
        Position(10, 15, 7),
        Position(15, 10, 0),
        Position(20, 12, 3),
        Position(0, -3, 13),
    )

    assert fast_cycle_length(state) == 478373365921244
