from typing import List


def path_to_coordinates(
    path: List[str], coordinates: dict = None, previous_position=(0, 0), previous_step=1
) -> dict:
    coordinates = coordinates if coordinates else dict()

    if not path:
        return coordinates

    x, y = previous_position
    direction, distance = path[0][0], int(path[0][1:])

    for step in range(previous_step, previous_step + distance):
        if direction == "R":
            x += 1
        elif direction == "L":
            x -= 1
        elif direction == "U":
            y += 1
        elif direction == "D":
            y -= 1
        else:
            raise ValueError("Bad direction")

        if (x, y) not in coordinates:
            coordinates[(x, y)] = step

    return path_to_coordinates(path[1:], coordinates, (x, y), previous_step + distance)


def manhattan(coord):
    x, y = coord
    return abs(x) + abs(y)


def intersections(path1: List[str], path2: List[str]) -> set:
    path1_coords = path_to_coordinates(path1)
    path2_coords = path_to_coordinates(path2)

    return set(path1_coords.keys()) & set(path2_coords.keys())


def nearest_intersection(path1, path2):
    return min(intersections(path1, path2), key=lambda coord: manhattan(coord))


def intersections_with_path_length(path1, path2) -> dict:
    path1_coords = path_to_coordinates(path1)
    path2_coords = path_to_coordinates(path2)

    intersections = set(path1_coords.keys()) & set(path2_coords.keys())
    return {coord: path1_coords[coord] + path2_coords[coord] for coord in intersections}

def shortest_intersection_path_length(path1, path2):
    return min(intersections_with_path_length(path1, path2).values())

def parse_path(path_spec):
    return path_spec.split(",")


if __name__ == "__main__":
    with open("input") as fp:
        path_spec1, path_spec2 = fp.readlines()

        path1 = parse_path(path_spec1)
        path2 = parse_path(path_spec2)

        assert path1[5] == "U457"
        assert path2[6] == "L878"

        print(manhattan(nearest_intersection(path1, path2)))
        print(shortest_intersection_path_length(path1, path2))
