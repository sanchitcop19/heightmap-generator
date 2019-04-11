import requests
import json
import sys
import time
import numpy as np
from decimal import Decimal

offset = 100000
#offset = 10000

#bottom_left_lat = 0
#bottom_left_lon = 0

bottom_left_lat = 42.29906
bottom_left_lon = -83.69991
#--------------------------------
# temp
#bottom_left_lat = 43.2990
#bottom_left_lon = -83.6999
#--------------------------------
#bottom_right_lat = bottom_left_lat
#bottom_right_lon = 8
bottom_right_lat = bottom_left_lat
bottom_right_lon = -83.69642
#--------------------------------
# temp
#bottom_right_lat = bottom_left_lat
#bottom_right_lon = -83.6964
#--------------------------------
#top_left_lat = 8
#top_left_lon = bottom_left_lon
#--------------------------------
top_left_lat = 42.30277777
top_left_lon = bottom_left_lon
# temp
#top_left_lat = 42.3027
#top_left_lon = bottom_left_lon
#--------------------------------
top_right_lat = top_left_lat
top_right_lon = bottom_right_lon
#--------------------------------
# temp
#top_right_lat = top_left_lat
#top_right_lon = bottom_right_lon
#--------------------------------

start_lon = int(top_left_lon*offset)
end_lon = int(top_right_lon*offset)

start_lat = int(top_left_lat*offset)
end_lat = int(bottom_left_lat*offset)
count = 0
length = 0
minimum = 12000
maximum = 0
#matrix = np.loadtxt("test.txt")
success = False
from random import randint
side = 8
#matrix = [[c for c in range(350)]for r in range(370)]
matrix = np.loadtxt('heightmap_precise_google.txt')
#print(matrix)
#print(start_lat, end_lat, start_lon, end_lon)
'''
for row, latitude in enumerate(range(start_lat, end_lat, -1)):
    length += 1
    for col, longitude in enumerate(range(start_lon, end_lon)):
        lat = latitude/offset
        lon = longitude/offset
        count += 1
        print(row, col)
        matrix[row][col] = 266 if col < 4 else 278
np.savetxt("dummy.txt", np.matrix(matrix))
'''

for row, latitude in enumerate(range(4230080, end_lat + 1, -1), start=197):
    length += 1
    for col, longitude in enumerate(range(start_lon, end_lon + 1)):
        lat= latitude/offset
        lon= longitude/offset
        print(lat, lon)

        count += 1
        #print(count)
        while not success:
            try:
                #r = requests.get('https://nationalmap.gov/epqs/pqs.php?x=' + str(lon) + '&y=' + str(lat) + '&units=Meters&output=json')
                r = requests.get('https://maps.googleapis.com/maps/api/elevation/json?locations=' + str(lat) + ','+str(lon)+apikey)

                elevation = json.loads(r.content)
                elevation = elevation['results'][0]['elevation']
                #print(elevation)
                if elevation < minimum:
                    minimum = elevation
                if elevation > maximum:
                    maximum = elevation

                matrix[row, col] = elevation
                print(elevation)
                success = True
                print(60550-count, " to go")
            except Exception as e:
                print(e)
                time.sleep(2)
                success = False
        success = False
    time.sleep(3)
    np.savetxt("heightmap_precise_google.txt", matrix)

print(count, " queries")
width = count/length
print("Length: ", length, "Width: ", width)
print("Maximum: ", maximum, "Minimum: ", minimum)
print(matrix)
