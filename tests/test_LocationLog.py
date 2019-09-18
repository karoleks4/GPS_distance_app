import pytest
from Location import Location
from LocationLog import LocationLog

# attribute assignment test data (passing)
valdata = [
	("data/customers.txt", [12, 1, 2, 3, 28, 7, 8, 26, 27, 6, 9, 10, 4, 5, 11, 31, 13, 14, 15, 16, 17, 39, 18, 24, 19, 20, 21, 22, 29, 30, 23, 25]),
]

# attribute assignment test data (failing)
valdata_fail = [
	("data/dontexist.txt"),
	("data/wrongformat.txt")
]

# add_customer test data
adddata = [
	("data/customers.txt", Location("Test", 51.509865, -0.118092), 99),
	("data/customers.txt", Location("Test", 51.509865, -0.118092), -1),
	("data/customers.txt", Location("Test", 51.509865, -0.118092), 0),
	("data/customers.txt", Location("Test", 51.509865, -0.118092), 12),
]

# remove_customer test data
removedata = [
	("data/customers.txt", 12),
	("data/customers.txt", 100),
	("data/customers.txt", -2),
]

# reduce_to_range test data
reducedata = [
	("data/customers.txt", Location("Dublin", 53.339428, -6.257664), 100, "data/expected.txt"),
	("data/customers.txt", Location("Dublin", 53.339428, -6.257664), 2000, "data/customers.txt"),
	("data/customers.txt", Location("Dublin", 53.339428, -6.257664), 0, "data/empty.txt"),
	("data/customers.txt", Location("Dublin", 53.339428, -6.257664), -100, "data/empty.txt")
]

class TestLocationLog:
	# test for correct class attribute assignment
	@pytest.mark.parametrize("filename, keys", valdata)
	def test_initial_value(self, filename, keys):
		customers = LocationLog(filename)
		assert len(customers.location_log.keys()) == len(keys)
		for k in customers.location_log.keys():
			assert k in keys

	# test for illegal class attribute assignment
	@pytest.mark.parametrize("filename", valdata_fail)
	def test_illegal_value(self, filename):
		with pytest.raises(Exception):
			LocationLog(filename)

	# test for adding entry to the log
	@pytest.mark.parametrize("filename, loc, idx", adddata)
	def test_add_customer(self, filename, loc, idx):
		customers = LocationLog(filename)
		customers.add_customer(loc,idx)
		assert customers.location_log[idx] == loc

	# test for removing entry from the log
	@pytest.mark.parametrize("filename, idx", removedata)
	def test_remove_customer(self, filename, idx):
		customers = LocationLog(filename)
		customers.remove_customer(idx)
		assert idx not in customers.location_log.keys()

	# test for log thresholding
	@pytest.mark.parametrize("filename, loc, thr, expected", reducedata)
	def test_reduce_to_range(self, filename, loc, thr, expected):
		customers = LocationLog(filename)
		customers.reduce_to_range(loc, thr)
		actual = LocationLog(expected)
		for i in customers.location_log.keys():
			assert customers.location_log[i].name == actual.location_log[i].name
			assert customers.location_log[i].latitude == actual.location_log[i].latitude
			assert customers.location_log[i].longitude == actual.location_log[i].longitude