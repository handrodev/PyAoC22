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

        if by == at_y: beacons_at_y.add(b)
        if sy == at_y: sensors_at_y += 1

        # Consider only sensors close enough to (at_y) to be relevant, i.e.
        # where the manhattan distance is <= abs(s.y - at_y)
        if abs(s.y - at_y) <= sb_dist:
            S[s] = b
            
    # Number of beacons at row Y
    # Length of the set of unique beacons at that row
    beacons_at_y = len(beacons_at_y)

    # Get the ranges of X (columns) covered by each sensor at row Y
    x_ranges = []
    
    for s, b in S.items():
        d = manhattan_dist(s, b)
        dist_to_y = abs(at_y - s.y)
        width = d - dist_to_y
        if width > 0:
            min_x = s.x - width
            max_x = s.x + width

            x_ranges.append((min_x, max_x))

    # Combine found ranges into the minimal subset of non-overlapping ranges
    x_ranges.sort()
    result = []
    z1, z2 = x_ranges[0]
    for x1, x2 in x_ranges:
        if x1 <= z2 < x2:
            z2 = x2
        elif x1 > z2:
            result.append((z1, z2))
            z1 = x1
            z2 = x2
    
    result.append((z1, z2))
    no_beacons = sum([max_x - min_x + 1 for min_x, max_x in result])

    # Subtract number of beacons and sensors at Y and return count
    return no_beacons - beacons_at_y - sensors_at_y

def part2(input, max_coord=20):
    # Parse input
    # Map of (relevant) sensors
    # Key <Position> : Value <Closest beacon> (required to compute X ranges covered at Y)
    S = {}
    regex = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

    for line in input:
        data = list(map(int, regex.findall(line)[0]))
        sx, sy = data[0:2]
        s = Point(sx, sy)

        bx, by = data[2:]
        b = Point(bx, by)

        S[s] = b

    def find_beacons(at_y=10):
        """
        Find any beacons and return the X position of the first beacon found
        If no possible beacons are found, return -1
        """
        # Get the ranges of X (columns) covered by each sensor at row Y
        x_ranges = []
        
        for s, b in S.items():
            d = manhattan_dist(s, b)
            dist_to_y = abs(at_y - s.y)
            width = d - dist_to_y
            if width > 0:
                min_x = s.x - width
                max_x = s.x + width

                x_ranges.append((min_x, max_x))
        
        # Combine found ranges into the minimal subset of non-overlapping ranges
        x_ranges.sort()
        result = []
        z1, z2 = x_ranges[0]
        for x1, x2 in x_ranges:
            if x1 <= z2 < x2:
                z2 = x2
            elif x1 > z2:
                result.append((z1, z2))
                z1 = x1
                z2 = x2
        
        result.append((z1, z2))

        x_beacon = -1
        if len(result) > 1:
            # Found a possible position for a beacon (between two ranges)
            x_beacon = result[1][0] - 1
        
        return x_beacon

    for y in range(0, max_coord + 1):
        beacon_x = find_beacons(at_y=y)
        if beacon_x != -1:
            break

    return beacon_x * 4000000 + y

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines, at_y=2000000))
    print(part2(lines, max_coord=4000000))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", lambda x: part1(x, at_y=10), 26)
    test_part(f"data/{filename}_test.txt", lambda x: part2(x, max_coord=20), 56000011)
    main(f"data/{filename}.txt")