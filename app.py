from Location import Location
from LocationLog import LocationLog

if __name__ == "__main__":
	# location of Dublin
	dublin = Location("Dublin", 53.339428, -6.257664)

	# process customers' locations
	customers = LocationLog("data/customers.txt")
	# threshold locations (<= 100 km)
	customers.reduce_to_range(dublin, 100.0)
	# save data in .txt file
	customers.save_to_file("data/output.txt")