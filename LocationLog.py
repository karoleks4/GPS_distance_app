import json
from Location import Location
from utils.distances import vincenty

class LocationLog:
	"""Class used to present a log of locations

	Args:
		location_log (dict): location log
	"""
	location_log = dict()

	def __init__(self, filename = None):
		"""Class constructor.

		Args:
			filename (str): name of the .txt file to generate log from (default = None)
		"""
		if filename is None:
			pass
		else:
			try:
				file = open(filename, 'r')
			except:
				raise 
			
			for entry in file.readlines():
				try:
					data = json.loads(entry)
					loc = Location(data['name'], float(data['latitude']), float(data['longitude']))
					idx = data['user_id']
					self.add_customer(loc, idx)
				except:
					raise

	def add_customer(self, loc, idx):
		"""Adds customer entry to the log.

		Args:
			loc (Location): location 
			idx (int): index in the log
		"""
		self.location_log[idx] = loc

	def remove_customer(self, idx):
		"""Removes customer entry from the log if it exists.

		Args:
			idx (int): index in the log
		"""
		try:
			del self.location_log[idx]
		except KeyError:
			print("Entry with ID {} does not exist".format(idx))
			pass

	def reduce_to_range(self, loc, thr):
		"""Removes all log entries that are farther 
		from the location by the threshold distance

		Args:
			loc (Location): location 
			thr (float): threshold distance (in km)
		"""
		tmp = dict(self.location_log)
		for idx, customer in tmp.items():
			dist = vincenty(customer, loc)
			if dist > thr:
				self.remove_customer(idx)

	def save_to_file(self, filename):
		"""Saves the results to the filename.txt file sorted by user_ids 
		in ascending order in a '{"user_id": #, "name": #}' format

		Args:
			filename (str): name of the output .txt file
		"""
		with open(filename, 'w+') as text_file:
			for idx in sorted(self.location_log.keys()):
				text_file.write('{{"user_id": {0}, "name": {1}}}\n'.format(idx, self.location_log[idx].name))

