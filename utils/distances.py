""" Different measures of calculating great circle distance 
between two given locations (in km).
"""

from math import radians, cos, sin, asin, tan, atan, atan2, sqrt
from geopy import distance
from Location import Location

# Haversine formula constants
EARTH_RADIUS = 6371.0088
# Vincenty's formula constants
MAJOR_AXIS = 6378137.0
FLATTENING = 1 / 298.257223563
MINOR_AXIS = (1 - FLATTENING) * MAJOR_AXIS

def haversine(loc1, loc2):
	"""Calculates great circle distance between two locations based on Haversine formula:
	https://en.wikipedia.org/wiki/Haversine_formula.
	Used as a first version of the project but proves to be inaccurate.

	Args:
		loc1, loc2 (Location): Location objects reprsenting desired locations

	Returns:
		float: great circle distance between loc1 and loc2
	"""
	lon1 = loc1.longitude
	lat1 = loc1.latitude
	lon2 = loc2.longitude
	lat2 = loc2.latitude
	
	# convert degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula 
	d_lon = lon2 - lon1 
	d_lat = lat2 - lat1 
	d_sig = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
	d_sig = 2 * asin(sqrt(d_sig))

	return d_sig * EARTH_RADIUS

def vincenty(loc1, loc2, steps = 150):
	"""Calculates great circle distance between two locations based on Vincenty's formula:
	https://en.wikipedia.org/wiki/Vincenty%27s_formulae
	Much more accurate than Haversine formula.

	Args:
		loc1, loc2 (Location): Location objects reprsenting desired locations
		steps (float): maximum number of iterations (default = 150)

	Returns:
		float: great circle distance between loc1 and loc2
	"""
	if steps < 0:
		raise ValueError("Number of iterations cannot be negative")

	# convert degrees to radians
	phi_1, L_1, phi_2, L_2 = map(radians, [loc1.latitude, loc1.longitude, loc2.latitude, loc2.longitude])
	
	# compare the same locations
	if phi_1 == phi_2 and L_1 == L_2 :
		return 0

	# Vincenty's formula
	# prepare parameters
	L = L_2 - L_1
	Lambda = L
	U_1 = atan((1 - FLATTENING) * tan(phi_1))
	U_2 = atan((1 - FLATTENING) * tan(phi_2))
	
	sin_U1 = sin(U_1)
	cos_U1 = cos(U_1)
	sin_U2 = sin(U_2)
	cos_U2 = cos(U_2)
	
	# start iterating
	ctr = 0
	while ctr < steps:
		ctr += 1
		
		sin_sig = sqrt((cos_U2 * sin(Lambda)) ** 2 + (cos_U1 * sin_U2 - sin_U1 * cos_U2 * cos(Lambda)) ** 2)
		cos_sig = sin_U1 * sin_U2 + cos_U1 * cos_U2 * cos(Lambda)
		sig = atan2(sin_sig, cos_sig)
		sin_a = (cos_U1 * cos_U2 * sin(Lambda)) / sin_sig
		cos_sq_a = 1 - sin_a ** 2
		cos_2sigm = cos_sig - ((2 * sin_U1 * sin_U2) / cos_sq_a)
		C = (FLATTENING / 16) * cos_sq_a * (4 + FLATTENING * (4 - 3 * cos_sq_a))
		tmp = Lambda
		Lambda = L + (1 - C) * FLATTENING * sin_a * (sig + C * sin_sig * (cos_2sigm + C * cos_sig * (-1 + 2 * cos_2sigm ** 2)))
		# check convergence (10 ** −12 corresponds to approximately 0.06 mm; standard convention)
		if abs(tmp - Lambda) <= 10**-12:
			break
	
	U_sq = cos_sq_a * ((MAJOR_AXIS ** 2 - MINOR_AXIS ** 2) / MINOR_AXIS ** 2)   
	A = 1 + (U_sq / 16384) * (4096 + U_sq * (-768 + U_sq * (320 - 175 * U_sq)))
	B = (U_sq / 1024) * (256 + U_sq * (-128 + U_sq * (74 - 47 * U_sq)))
	d_sig = B * sin_sig * (cos_2sigm + (1/4) * B * (cos_sig * (-1 + 2 * cos_2sigm ** 2) - (1/6) * B * cos_2sigm * (-3 + 4 * sin_sig ** 2) * (-3 + 4 * cos_2sigm ** 2)))

	return MINOR_AXIS * A * (sig - d_sig) / 1000

def geopy_dist(loc1, loc2):
	"""Calculates great circle distance between two locations using a geopy build-in function:
	https://geopy.readthedocs.io/en/latest/#module-geopy.distance
	Used for comparison.

	Args:
		loc1, loc2 (Location): Location objects reprsenting desired locations

	Returns:
		float: great circle distance between loc1 and loc2
	"""
	cloc1 = (loc1.latitude, loc1.longitude)
	cloc2 = (loc2.latitude, loc2.longitude)
	return distance.distance(cloc1, cloc2).km
