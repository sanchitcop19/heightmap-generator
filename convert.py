import sys
import png
import numpy as np
from numpy.testing import assert_almost_equal
from random import randint
from time import time
from bisect import bisect_left, bisect_right


def run():

    class KeyList(object):
        # Source: Don't remember, TODO
        # bisect doesn't accept a key function, so we build the key into our sequence.
        def __init__(self, l, key):
            self.l = l
            self.key = key

        def __len__(self):
            return len(self.l)

        def __getitem__(self, index):
            return self.key(self.l[index])

    def find_bounds(matrix):
        """
        Since white represents the highest point in the elevation matrix
        and black represents the lowest, the minimum and maximum elevation
        is needed to generate the relative coloring
        """
        return np.amin(matrix), np.amax(matrix)

    def map_color(matrix):
        """

        """
        temp = np.zeros((len(matrix[0])), dtype=object)
        for idx, element in enumerate(matrix[0]):
            temp[idx] = (idx, element)
        return temp

    def create_elevation_vector(matrix):
        """
        Generates a vector of elevations from the lowest to the highest 
        elevation by dividing the range into equal parts. The total possible
        elevations that can be represented are 2**bitdepth
        """
        start, stop = find_bounds(matrix)
        elevations = np.linspace(start, stop, 2 ** bitdepth, retstep=True)

        return elevations

    def find_le(a, x):
        # Source: Python docs
        'Find rightmost value less than or equal to x'
        i = bisect_right(a, x)
        if i:
            return a[i - 1]
        raise ValueError

    def find_ge(a, x):
        # Source: Python docs
        'Find leftmost item greater than or equal to x'
        i = bisect_left(a, x)
        if i != len(a):
            return a[i]
        raise ValueError

    # Change this as you see fit, a bitdepth of 16 implies you can use 2**16
    # or 65536 possible colors for the heightmap
    bitdepth = 16

    # Load the matrix from the txt file saved using query.py
    matrix = np.loadtxt(sys.argv[2])

    # See the function docstring
    possible_colors = create_elevation_vector(matrix)

    # See the function docstring
    assignment = map_color(possible_colors)
    
    rows = cols = int(sys.argv[1])
    heightmap = np.zeros((rows, cols), dtype=int)

    for row in range(0, rows):
        for col in range(0, cols):

            # Arbitrary assignment of a specific elevation to the closest color we
            # can represent using the elevation vector, found using binary search
            left = find_ge(possible_colors[0], matrix[row, col])
            right = find_le(possible_colors[0], matrix[row, col])

            color = left if abs(left-matrix[row, col]) < abs(right-matrix[row, col]) else right

            # Maps elevation to the appropriate color and assigns it to the heightmap matrix
            heightmap[row, col] = bisect_left(KeyList(assignment, key = lambda x : x[1]), color)

    np.savetxt(sys.argv[3], heightmap)

    with open(sys.argv[4], 'wb') as file:
        w = png.Writer(width = cols, height = rows, greyscale=True, bitdepth=bitdepth)
        w.write(file, heightmap.tolist())


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 convert.py <side> <heightmap txt> <heightmap-output txt> <image>")
        sys.exit(1)
    run()