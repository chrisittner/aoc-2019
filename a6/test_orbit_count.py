from .orbit_count import OrbitMap

orbit_map_str = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

om = OrbitMap(orbit_map_str)


def test_parse():
    print(om.objects)
    assert om.direct_orbits == {
        "B": "COM",
        "C": "B",
        "D": "C",
        "E": "D",
        "F": "E",
        "G": "B",
        "H": "G",
        "I": "D",
        "J": "E",
        "K": "J",
        "L": "K",
    }
    assert set(om.objects) == {"B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"}


def test_orbits():
    assert om.orbits("D") == ["C", "B", "COM"]
    assert om.orbits("L") == ["K", "J", "E", "D", "C", "B", "COM"]
    assert om.orbits("COM") == []


def test_total_orbit_count():
    assert om.total_orbit_count() == 42


def test_part1():
    with open("input") as fp:
        om = OrbitMap(fp.read())
        assert om.total_orbit_count() == 142497


orbit_map2_str = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""
om2 = OrbitMap(orbit_map2_str)


def test_num_orbital_transfers():
    assert om2.num_orbital_transfers("YOU", "SAN") == 4
