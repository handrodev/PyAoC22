import sys
import os
import re

from Utils import *
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

def manhattan_dist(pt_1: Point, pt_2: Point):
    return abs(pt_1.x - pt_2.x) + abs(pt_1.y - pt_2.y)

def part1(input, at_y=10):
    regex = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    
    # Map of (relevant) sensors
    # Key <Position> : Value <Distance to closest beacon> (required to compute X ranges covered at Y)
    S = {}

    beacons_at_y = set()
    sensors_at_y = 0
    for line in input:
        data = list(map(int, regex.findall(line)[0]))
        sx, sy = data[0:2]
        s = Point(sx, sy)

        bx, by = data[2:]
        b = Point(bx, by)

        sb_dist = manhattan_dist(s, b)

        if by == at_y:
            beacons_at_y.add(b)

        if sy == at_y:
            sensors_at_y += 1

        # Consider only sensors close enough to (at_y) to be relevant, i.e.
        # where the manhattan distance is <= abs(s.y - at_y)
        if abs(s.y - at_y) <= sb_dist:
            S[Point(sx, sy)] = sb_dist
            
    # Number of beacons at row Y
    # Length of the set of unique beacons at that row
    beacons_at_y = len(beacons_at_y)

    # Get the ranges of X (columns) covered by each sensor at row Y
    x_ranges = []
    # And also keep track of global minimum and maximum
    # These determine the range of columns to look at
    gmin_x = float('+inf')
    gmax_x = float('-inf')
    
    for s, d in S.items():
        dist_to_y = abs(at_y - s.y)
        width = d - dist_to_y
        min_x = s.x - width
        max_x = s.x + width
        
        if min_x < gmin_x: gmin_x = min_x
        if max_x > gmax_x: gmax_x = max_x

        x_ranges.append((min_x, max_x))

    no_beacons = 0
    
    # For each relevant column (X)
    for x in range(gmin_x, gmax_x + 1):
        # Check the X ranges of each sensor
        for min_x, max_x in x_ranges:
            # If the current cell is covered by some sensor
            # There cannot be a beacon here, count it as no_beacon and break
            if min_x <= x <= max_x:
                no_beacons += 1
                break

    # Subtract number of beacons and sensors at Y and return count
    return no_beacons - beacons_at_y - sensors_at_y

def part2(input):
    return len(input)

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines, at_y=2000000))
    # print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", lambda x: part1(x, at_y=10), 26)
    # test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")