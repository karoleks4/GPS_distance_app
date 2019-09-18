import pytest
from Location import Location

# passing cases
passdata = [
	(53.339428, -6.257664, Location("Test", 53.339428, -6.257664)),
	(-1, 0, Location("Test", -1, 0)),
    (90, 180, Location("Test", 90, 180)),
    (-90, -180, Location("Test", -90, -180)),
    (90, -180, Location("Test", 90, -180)),
    (-90, 180, Location("Test", -90, 180))
]

# failing cases 
faildata = [
	(2000, 3),
	(78, 183),
	(180, 90),
    (90.000001, 180),
    (-90, -180.000001),
    (90.000001, -180.000001),
    (-90.000001, 180.000001)
]

class TestLocation:
	# test for correct class attribute assignment  
	@pytest.mark.parametrize("lat, lon, expected", passdata)
	def test_initial_value(self, lat, lon, expected):
		loc = Location("Test", lat, lon)
		assert loc.name == expected.name
		assert loc.latitude == expected.latitude
		assert loc.longitude == expected.longitude

	# test for empty class attribute assignment
	def test_no_value(self):
		with pytest.raises(Exception):
			loc = Location()

	# test for partial class attribute assignment
	@pytest.mark.parametrize("lat, lon, expected", passdata[:1])
	def test_partial_value(self, lat, lon, expected):
		with pytest.raises(Exception):
			loc = Location("Test", lon)
		with pytest.raises(Exception):
			loc = Location("Test", lat)
		with pytest.raises(Exception):
			loc = Location(lon, lat)

	# test for class attribute assignment order
	@pytest.mark.parametrize("lat, lon, expected", passdata[:2])
	def test_swap_value(self, lat, lon, expected):
		loc1 = Location("Test", lat, lon)
		loc2 = Location("Test", lon, lat)
		assert loc1.name == loc2.name
		assert loc1.latitude != loc2.latitude
		assert loc1.longitude != loc2.longitude

	# test for class attribute illegal value assignment
	@pytest.mark.parametrize("lat, lon", faildata)
	def test_illegal_value(self, lat, lon):
		with pytest.raises(Exception):
			loc = Location("Test", lat, lon)
