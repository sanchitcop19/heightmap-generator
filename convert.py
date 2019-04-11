import sys
import png
import numpy as np
from numpy.testing import assert_almost_equal
from random import randint
from time import time
from bisect import bisect_left, bisect_right


def run():
    class KeyList(object):
        # bisect doesn't accept a key function, so we build the key into our sequence.
        def __init__(self, l, key):
            self.l = l
            self.key = key

        def __len__(self):
            return len(self.l)

        def __getitem__(self, index):
            return self.key(self.l[index])

    if len(sys.argv) < 4:
        print("not enough arguments given")
        sys.exit()
    def find_bounds(matrix):
        return np.amin(matrix), np.amax(matrix)

    def map_color(matrix):
        temp = np.zeros((len(matrix[0])), dtype=object)
        for idx, element in enumerate(matrix[0]):
            temp[idx] = (idx, element)
        return temp

    def create_colors(matrix):
        start, stop = find_bounds(matrix)
        #lowest elevation to highest, 655side colors
        save = np.linspace(start, stop, 2 ** bitdepth, retstep=True)
        print(save)

        return save

    def find_le(a, x):
        'Find rightmost value less than or equal to x'
        i = bisect_right(a, x)
        if i:
            return a[i - 1]
        raise ValueError

    def find_ge(a, x):
        'Find leftmost item greater than or equal to x'
        i = bisect_left(a, x)
        if i != len(a):
            return a[i]
        raise ValueError

    bitdepth = 16

    matrix = np.loadtxt(sys.argv[1])

    possible_colors = create_colors(matrix)

    assignment = map_color(possible_colors)
    #iterate through each
    # find closest mapping in possible_colors
    # assign a new numpy array that coloring
    rows = 257
    cols = 257
    heightmap = np.zeros((rows, cols), dtype=int)
    for row in range(0, rows):
        for col in range(0, cols):
            left = find_ge(possible_colors[0], matrix[row, col])
            right = find_le(possible_colors[0], matrix[row, col])
            print("row, col: ", row, col)
            color = left if abs(left-matrix[row, col]) < abs(right-matrix[row, col]) else right
            heightmap[row, col] = bisect_left(KeyList(assignment, key = lambda x : x[1]), color)

    np.savetxt(sys.argv[2], heightmap)
    save = heightmap.tolist()

    with open(sys.argv[3], 'wb') as file:
        w = png.Writer(width = cols, height = rows, greyscale=True, bitdepth=bitdepth)
        w.write(file, heightmap.tolist())

    # print(time()-start)


if __name__ == "__main__":
    run()

# -TRASH-------------------------------------------------------------------------------

'''
    start = time()
    side = 2**bitdepth
    #s = [[x for x in range(2**bitdepth)] for y in range(2**bitdepth)]
    side_copy = 352
    s = np.fromfunction(lambda x, y: y + 120*x, (side_copy, side_copy), dtype=int)
    #s = np.random.randint(side, size = (side_copy,side_copy)).tolist()
    #print(s)
'''
