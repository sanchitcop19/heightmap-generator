import requests
import json
import sys
import time
import numpy as np
from decimal import Decimal
from math import inf
from config import *

"""
IMPORTANT: The generator works for rectangular heightmaps only.
"""
if len(sys.argv) < 3:
    print("Usage: python3 query.py <rows> <columns>")
    sys.exit(1)

# Set the dimensions of the heightmap
rows  = int(sys.argv[1])
columns = int(sys.argv[2])

# Add a check for precision

# Converts the decimal degrees to an integer temporarily
offset = 10 ** len(str(Decimal(str(TOP_LEFT_LAT))).split('.')[1])

start_lon = int(TOP_LEFT_LON * offset)
end_lon = int(TOP_RIGHT_LON * offset)

start_lat = int(TOP_LEFT_LAT * offset)
end_lat = int(BOTTOM_LEFT_LAT * offset)

count = 0
length = 0

minimum = inf
maximum = 0

success = False

total_queries = rows*columns

matrix = np.array([[c for c in range(columns)]for r in range(rows)], dtype = 'float64')

# Uncomment below if you want to load a partially saved heightmap
#matrix = np.loadtxt('heightmap.txt')

for row, latitude in enumerate(range(start_lat, end_lat + 1, -1)):

    length += 1

    for col, longitude in enumerate(range(start_lon, end_lon + 1)):

        lat = latitude / offset
        lon = longitude / offset
        print("-----------------------------------")
        print("Coordinates: (", lat, ", ", lon, ")")
        count += 1

        while not success:
            try:
                # Uncomment the line below to use the USGS service instead
                # r = requests.get('https://nationalmap.gov/epqs/pqs.php?x=' \
                # + str(lon) + '&y=' + str(lat) + '&units=Meters&output=json')
                query = 'https://maps.googleapis.com/maps/api/elevation/json?locations=' + str(lat) + ',' + str(lon) + '&key=' + APIKEY

                r = requests.get(query)

                elevation = json.loads(r.content)
                elevation = elevation['results'][0]['elevation']

                minimum = elevation if elevation < minimum else minimum

                maximum = elevation if elevation > maximum else maximum

                matrix[row, col] = elevation

                print(total_queries - count, "queries to go")


                success = True

            except Exception as e:
                # Catch every exception and try again, the internet is an unreliable abyss :)
                print(e)
                time.sleep(1)
                success = False
        success = False

    # Saving the data after every row is done, the file is overwritten each time
    np.savetxt("heightmap.txt", matrix)

print(count, " queries were made.")
width = count / length
print("Dimensions of the heightmap:")
print("Length: ", length, "Width: ", width)
print("Maximum elevation: ", maximum, "Minimum elevation: ", minimum)
