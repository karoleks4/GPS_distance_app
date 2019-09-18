import pytest
from Location import Location
from utils.distances import haversine, vincenty, geopy_dist
from geopy import distance

# testing value cases
testdata = [
	(Location("Test1", 53.339428, -6.257664), Location("Test3", 53.997945, -6.405957)),
	(Location("Test2", 51.509865, -0.118092), Location("Test1", 53.339428, -6.257664)),
	(Location("Test3", 53.997945, -6.405957), Location("Test2", 51.509865, -0.118092))
]

# testing step variable cases
stepsdata = [
	(Location("Test1", 53.339428, -6.257664), Location("Test3", 53.997945, -6.405957), 150),
	(Location("Test2", 51.509865, -0.118092), Location("Test1", 53.339428, -6.257664), -10),
	(Location("Test3", 53.997945, -6.405957), Location("Test2", 51.509865, -0.118092), 0)
]

class TestDistances:
	# test for swapped locations (iterative method might encounter possible rounding errors)
	@pytest.mark.parametrize("loc1, loc2", testdata)
	def test_swapped(self, loc1, loc2):
		diff = abs(vincenty(loc1, loc2) - vincenty(loc2, loc1))
		assert diff < 10 ** -11 # accounting for possible rounting errors

	# test for the same location
	@pytest.mark.parametrize("loc1, loc2", testdata)
	def test_same(self, loc1, loc2):
		assert vincenty(loc1, loc1) == 0
		assert vincenty(loc2, loc2) == 0

	# test for accuracy (compared to geopy built-in method)
	@pytest.mark.parametrize("loc1, loc2", testdata)
	def test_accuracy(self, loc1, loc2):
		diff = abs(vincenty(loc1, loc2) - geopy_dist(loc1, loc2))
		assert diff <= 10 ** -4 # accuracy to 1 meter

	# test for default steps parameter
	@pytest.mark.parametrize("loc1, loc2, steps", stepsdata[:1])
	def test_default_steps(self, loc1, loc2, steps):
		assert vincenty(loc1, loc1, steps) == vincenty(loc1, loc1)

	# test for illegal steps parameter
	@pytest.mark.parametrize("loc1, loc2, steps", stepsdata[1:])
	def test_illegal_steps(self, loc1, loc2, steps):
		with pytest.raises(Exception):
			assert vincenty(loc1, loc1, steps)
