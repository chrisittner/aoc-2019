import math


def fuel_for_mass(mass):
    return math.floor(mass / 3) - 2


def total_fuel_for_mass(mass):
    fuel = fuel_for_mass(mass)

    if fuel > 0:
        total_fuel = fuel + total_fuel_for_mass(fuel)
    else:
        total_fuel = 0
    return total_fuel


if __name__ == "__main__":
    with open("input") as fp:
        masses = [int(mass) for mass in list(fp)]
        assert masses[2] == 119076

        fuel = sum([fuel_for_mass(mass) for mass in masses])
        print("Part 1: ", fuel)

        total_fuel = sum([total_fuel_for_mass(mass) for mass in masses])
        print("Part 2: ", total_fuel)
