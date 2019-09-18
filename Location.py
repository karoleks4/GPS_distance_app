class Location:
	"""Class used to present a GPS location

	Args:
		name (str): location name
		latitude (float): location latitude
		longitude (float): location longitude
	"""
	def __init__(self, name, latitude, longitude):
		"""
		Class constructor

		Args:
			name (str): location name
			latitude (float): location latitude (in decimal degrees; range of [-90,90])
			longitude (float): location longitude (in decimal degrees; range of [-180,180])
		"""
		self.name = name
		if abs(latitude) > 90.0:
			raise ValueError("Latitude value is invalid (i.e. not in [-90,90])")
		if abs(longitude) > 180.0:
			raise ValueError("Longitude value is invalid (i.e. not in [-180,180])")
		self.latitude = latitude
		self.longitude = longitude