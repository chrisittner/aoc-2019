from typing import Iterable, Union, List


class OrbitMap:
    def __init__(self, direct_orbits: Union[dict, str]):
        self.direct_orbits = (
            direct_orbits if type(direct_orbits) is dict else self.parse(direct_orbits)
        )

    @staticmethod
    def parse(direct_orbits_str: str):
        return {
            orbit_info.split(")")[1]: orbit_info.split(")")[0]
            for orbit_info in direct_orbits_str.splitlines()
        }

    @property
    def objects(self) -> Iterable[str]:
        return self.direct_orbits.keys()

    def orbits(self, obj) -> List[str]:
        if obj not in self.direct_orbits:
            return []

        direct_orbit = self.direct_orbits[obj]
        return [direct_orbit] + self.orbits(direct_orbit)

    def total_orbit_count(self):
        return sum([len(self.orbits(obj)) for obj in self.objects])

    def num_orbital_transfers(self, source, dest) -> int:
        return len(set(self.orbits(source)) ^ set(self.orbits(dest)))


if __name__ == "__main__":
    with open("input") as fp:
        om = OrbitMap(fp.read())
        assert om.total_orbit_count() == 142497

        print(om.num_orbital_transfers("YOU", "SAN"))
