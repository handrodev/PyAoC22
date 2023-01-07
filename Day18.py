import sys
import os
from queue import Queue

from Utils import *


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


def has_path_to_ext(cube: tuple[int, int, int],
                    cubes: set[tuple[int, int, int]],
                    boundaries: tuple[int, int, int, int, int, int],
                    trapped: set[tuple[int, int, int]],
                    not_trapped: set[tuple[int, int, int]]) -> bool:
    """
    Returns True if the specified cube has a path to the exterior (not trapped) 
    and False otherwise (trapped)
    """
    q = Queue()
    q.put(cube)

    min_x, max_x, min_y, max_y, min_z, max_z = boundaries

    visited = set()
    while not q.empty():
        c = q.get()
        x, y, z = c

        if c in not_trapped:
            # Already know that this cube has a path to the environment
            return True

        if c in trapped or c in cubes:
            # Already know that this cube is trapped
            # or path is blocked by another cube
            continue

        if any([x > max_x, x < min_x, y > max_y, y < min_y, z > max_z, z < min_z]):
            return True

        for adj in adjacent(c):
            if adj not in visited:
                visited.add(adj)
                q.put(adj)

    # Could not find a path, cube is trapped
    return False


def compute_ext_surface(cubes: set[tuple[int, int, int]]) -> int:
    min_x, max_x = float('+inf'), float('-inf')
    min_y, max_y = float('+inf'), float('-inf')
    min_z, max_z = float('+inf'), float('-inf')

    for x, y, z in cubes:
        min_x, max_x = min(x, min_x), max(x, max_x)
        min_y, max_y = min(y, min_y), max(y, max_y)
        min_z, max_z = min(z, min_z), max(z, max_z)

    boundaries = (min_x, max_x, min_y, max_y, min_z, max_z)
    trapped = set([])
    not_trapped = set([])
    ext_surface = 0
    for c in cubes:
        for adj in adjacent(c):
            if has_path_to_ext(adj, cubes, boundaries, trapped, not_trapped):
                not_trapped.add(adj)
                ext_surface += 1
            else:
                trapped.add(adj)

    return ext_surface


def part1(input):
    cubes = set(parse_input(input))
    return compute_surface(cubes)


def part2(input):
    cubes = set(parse_input(input))
    return compute_ext_surface(cubes)


def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 64)
    test_part(f"data/{filename}_test.txt", part2, 58)
    main(f"data/{filename}.txt")
