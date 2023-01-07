import sys
import os

from Utils import *

from itertools import combinations


def adjacent(cube: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    """
    Returns the cubes adjacent to the current one
    """
    x, y, z = cube
    return set([(x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)])


def parse_input(input: list[str]) -> list[tuple[int, int, int]]:
    input = [l.strip() for l in input]
    return [tuple(map(int, c.split(","))) for c in input]


def compute_surface(cubes: set[tuple[int, int, int]]) -> int:
    # A free floating cube has 6 free faces
    # Thus, a cube with N adjacent cubes has 6 - N free faces
    # The total number of free faces (surface) is:
    surface = 0
    for c in cubes:
        # Count number of cubes adjacent to the current one
        # Reduce the free faces and add to cumulated surface
        surface += 6 - len(adjacent(c) & cubes)

    return surface


def part1(input):
    cubes = set(parse_input(input))
    return compute_surface(cubes)


def part2(input):
    return len(input)


def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return

    print(part1(lines))
    # print(part2(lines))


if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 64)
    # test_part(f"data/{filename}_test.txt", part2, 58)
    main(f"data/{filename}.txt")
