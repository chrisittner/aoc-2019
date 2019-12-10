from typing import Union, Tuple, List
import math as _math
import functools as _functools


class AsteroidMap:
    def __init__(self, _map: Union[str, list]):
        self.map = AsteroidMap.from_str(_map) if type(_map) == str else _map
        self.asteroids = self.get_asteroids()

    @staticmethod
    def from_str(map_str):
        return map_str.splitlines()

    def get_asteroids(self) -> List[Tuple[int, int]]:
        return [
            (x, y)
            for y, row in enumerate(self.map)
            for x, possible_location in enumerate(row)
            if possible_location == "#"
        ]

    @_functools.lru_cache()
    def visible_asteroids(self, location: Tuple[int, int]) -> List[Tuple[int, int]]:
        visible = []
        for asteroid in self.asteroids:
            if self.is_visible(location, asteroid):
                visible.append(asteroid)

        return visible

    def is_visible(
        self, location1: Tuple[int, int], location2: Tuple[int, int]
    ) -> bool:
        if not hasattr(self, "_visible_cache"):
            self._visible_cache = dict()

        if (location1, location2) not in self._visible_cache:
            self._visible_cache[(location1, location2)] = self.uncached_is_visible(
                location1, location2
            )

        return self._visible_cache[(location1, location2)]

    def uncached_is_visible(
        self, location1: Tuple[int, int], location2: Tuple[int, int]
    ) -> bool:
        if location1 == location2:
            return False

        direction, distance = self.to_polar(location1, location2)
        for asteroid in self.asteroids:
            if location1 == asteroid or location2 == asteroid:
                continue

            direction_of_ast, distance_of_ast = self.to_polar(location1, asteroid)
            if direction_of_ast == direction and 0 < distance_of_ast < distance:
                return False

        return True

    @staticmethod
    @_functools.lru_cache()
    def to_polar(location1, location2) -> Tuple[float, float]:
        assert not location1 == location2
        x, y = (location1[0] - location2[0], location1[1] - location2[1])

        angle = _math.atan2(y, x)
        distance = (x ** 2 + y ** 2) ** 0.5
        return angle, distance

    def max_number_of_visible_asteroids(self) -> Tuple[Tuple[int, int], int]:
        return max(
            [
                (asteroid, len(self.visible_asteroids(asteroid)))
                for asteroid in self.asteroids
            ],
            key=lambda x: x[1],
        )

    def visible_asteroids_sorted_by_angle(
        self, location: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        visible_asteroids = self.visible_asteroids(location)

        def translate_angle_to_sorting_order(angle):
            angle += _math.pi
            order = (angle + _math.pi / 2) % (2 * _math.pi)
            return order

        return sorted(
            visible_asteroids,
            key=lambda ast: translate_angle_to_sorting_order(
                self.to_polar(location, ast)[0]
            ),
        )


if __name__ == "__main__":
    with open("input_a10") as fp:
        map_str = fp.read()
        ast_map = AsteroidMap(map_str)

        assert ast_map.max_number_of_visible_asteroids() == ((31, 20), 319)
        print(ast_map.visible_asteroids_sorted_by_angle((31, 20))[199])
