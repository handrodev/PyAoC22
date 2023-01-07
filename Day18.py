import sys
import os

from Utils import *

from itertools import combinations


def adjacent(cube_1: tuple[int, int, int], cube_2: tuple[int, int, int]) -> bool:
    """
    Checks if two cubes are adjacent to each other
    """
    x1, y1, z1 = cube_1
    x2, y2, z2 = cube_2
    return any([
        x1 == x2 and y1 == y2 and (z1 == z2 + 1 or z1 == z2 - 1),
        (x1 == x2 + 1 or x1 == x2 - 1) and y1 == y2 and z1 == z2,
        x1 == x2 and (y1 == y2 + 1 or y1 == y2 - 1) and z1 == z2
    ])

def part1(input) -> int:
    input = [l.strip() for l in input]
    cubes = [tuple(map(int, c.split(","))) for c in input]

    # Matrix mapping a cube to its adjacent cubes (if any, otherwise an empty set)
    adj_mat = {c: set([]) for c in cubes}
    
    # Take combinations of 2 cubes without repetition
    for c1, c2 in combinations(cubes, 2):
        # If the two cubes are adjacent
        if adjacent(c1, c2):
            adj_mat[c1].add(c2)
            adj_mat[c2].add(c1)

    # A free floating cube has 6 free faces
    # Thus, a cube with N adjacent cubes has 6 - N free faces
    # The total number of free faces (surface) is:
    return sum([6 - len(adj) for adj in adj_mat.values()])

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
    # test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")