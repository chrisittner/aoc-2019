import pytest
from .wires import (
    path_to_coordinates,
    manhattan,
    intersections,
    nearest_intersection,
    parse_path,
    shortest_intersection_path_length
)


def test_path_to_coordinates():
    path = ["U2", "R2", "D2", "U2"]

    new_coordinates = path_to_coordinates(path)
    assert new_coordinates.keys() == {(0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)}
    assert new_coordinates == {(0, 1): 1, (0, 2): 2, (1, 2): 3, (2, 2): 4, (2, 1): 5, (2, 0): 6}

    coordinates = {(1, 1): 7}
    xy = (3, 3)

    new_coordinates = path_to_coordinates(path, coordinates, xy)
    assert new_coordinates.keys() == {(1, 1), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3)}
    assert new_coordinates == {(1, 1): 7, (3, 4): 1, (3, 5): 2, (4, 5): 3, (5, 5): 4, (5, 4): 5, (5, 3): 6}


def test_manhattan():
    assert manhattan((3, 4)) == 7


def test_intersections():
    path1 = ["R8", "U5", "L5", "D3"]
    path2 = ["U7", "R6", "D4", "L4"]

    assert intersections(path1, path2) == {(3, 3), (6, 5)}


@pytest.mark.parametrize(
    "path_spec1, path_spec2, dist",
    [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            135,
        ),
    ],
)
def test_dist_of_nearest_intersection(path_spec1, path_spec2, dist):
    path1 = parse_path(path_spec1)
    path2 = parse_path(path_spec2)
    assert manhattan(nearest_intersection(path1, path2)) == dist



@pytest.mark.parametrize(
    "path_spec1, path_spec2, dist",
    [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            135,
        ),
    ],
)
def test_dist_of_nearest_intersection(path_spec1, path_spec2, dist):
    path1 = parse_path(path_spec1)
    path2 = parse_path(path_spec2)
    assert manhattan(nearest_intersection(path1, path2)) == dist


@pytest.mark.parametrize(
    "path_spec1, path_spec2, step_count",
    [
        ("R8,U5,L5,D3", "U7,R6,D4,L4", 30),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 610),
        (
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            410,
        ),
    ],
)
def test_shortest_intersection_path_length(path_spec1, path_spec2, step_count):
    path1 = parse_path(path_spec1)
    path2 = parse_path(path_spec2)
    assert shortest_intersection_path_length(path1, path2) == step_count
