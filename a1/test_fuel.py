import pytest
from .fuel import fuel_for_mass, total_fuel_for_mass

@pytest.mark.parametrize("mass,fuel", [(12, 2), (14, 2), (1969, 654), (100756, 33583)])
def test_fuel_for_mass(mass, fuel):
    assert fuel_for_mass(mass) == fuel

@pytest.mark.parametrize("mass,total_fuel", [(12, 2), (14, 2), (1969, 966), (100756, 50346)])
def test_total_fuel_for_mass(mass, total_fuel):
    assert total_fuel_for_mass(mass) == total_fuel