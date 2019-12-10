import pytest
from .asteroids import AsteroidMap

test_map1 = AsteroidMap(
    """.#..#
.....
#####
....#
...##"""
)


def test_asteroids():
    assert test_map1.asteroids == [
        (1, 0),
        (4, 0),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (4, 3),
        (3, 4),
        (4, 4),
    ]


def test_is_visible():
    assert test_map1.is_visible((3, 2), (1, 0))
    assert test_map1.is_visible((1, 0), (3, 2))
    assert not test_map1.is_visible((1, 0), (4, 3))


def test_visible_asteroids():
    assert [
        len(test_map1.visible_asteroids(asteroid)) for asteroid in test_map1.asteroids
    ] == [7, 7, 6, 7, 7, 7, 5, 7, 8, 7]


def test_max_number_of_visible_asteroids():
    location, num_visible_asts = ((3, 4), 8)
    assert test_map1.max_number_of_visible_asteroids() == (location, num_visible_asts)


@pytest.mark.skip("Slow")
@pytest.mark.parametrize(
    "map_str, location, num_visible_asts",
    [
        (
            """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""",
            (5, 8),
            33,
        ),
        (
            """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""",
            (1, 2),
            35,
        ),
        (
            """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""",
            (6, 3),
            41,
        ),
        (
            """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""",
            (11, 13),
            210,
        ),
    ],
)
def test_max_number_of_visible_asteroids(map_str, location, num_visible_asts):
    ast_map = AsteroidMap(map_str)
    assert ast_map.max_number_of_visible_asteroids() == (location, num_visible_asts)


@pytest.mark.skip("Slow")
def test_part1():
    with open("input_a10") as fp:
        map_str = fp.read()
        ast_map = AsteroidMap(map_str)

        assert ast_map.max_number_of_visible_asteroids() == ((31, 20), 319)


def test_visible_ordered_by_angle():
    ast_map = AsteroidMap(
        """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""",
    )

    visible_by_angle = ast_map.visible_asteroids_sorted_by_angle((11, 13))

    visible = ast_map.visible_asteroids((11, 13))
    assert len(visible) == 210
    assert len(visible_by_angle) == 210

    print(ast_map.to_polar((11, 13), (11, 12)))
    print(ast_map.to_polar((11, 13), (19, 14)))

    assert visible_by_angle[:3] == [(11, 12), (12, 1), (12, 2)]
    assert visible_by_angle[9] == (12, 8)
    assert visible_by_angle[19] == (16, 0)
    assert visible_by_angle[49] == (16, 9)
    assert visible_by_angle[99] == (10, 16)
    assert visible_by_angle[198] == (9, 6)
    assert visible_by_angle[199] == (8, 2)
    assert visible_by_angle[200] == (10, 9)
