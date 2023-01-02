import sys
import os

from Utils import *
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
DRAW_SIMULATION = False

def normalize_paths(paths):
    """ 
    Normalize the specified paths so indexing starts at (0, 0)
    Return the normalized set of points covered by the specified paths
    and the width and height of the simulation grid
    """
    # Global minimum and maximum values
    gmin_x = float('+inf')
    gmin_y = float('+inf')
    gmax_x = -1
    gmax_y = -1

    # Determine minimum and maximum values of X and Y
    for path in paths:
        for point in path:
            if point.x < gmin_x:
                gmin_x = point.x
            if point.x > gmax_x:
                gmax_x = point.x
            if point.y < gmin_y:
                gmin_y = point.y
            if point.y > gmax_y:
                gmax_y = point.y
    
    rocks = set([])
    # For each path
    for i in range(1, len(paths)):
        # Each path contains segments determined by pairs of nodes
        for j in range(len(paths[i]) - 1):
            x1, y1 = paths[i][j]
            x2, y2 = paths[i][j+1]
            if x1 != x2:
                min_x = min(x1, x2)
                max_x = max(x1, x2)
                for k in range(min_x, max_x + 1):
                    rocks.add(Point(k - gmin_x, y1 - gmin_y))
            elif y1 != y2:
                min_y = min(y1, y2)
                max_y = max(y1, y2)
                for k in range(min_y, max_y + 1):
                    rocks.add(Point(x1 - gmin_x, k - gmin_y))

    w = (gmax_x - gmin_x) + 1
    h = (gmax_y - gmin_y) + 1
    
    sand_src = Point(paths[0][0].x - gmin_x, paths[0][0].y - gmin_y)

    return sand_src, rocks, w, h

def draw_state(w, h, rocks, sand, sand_src):
    """
    Draws the current state for the specified rocks and sand lists and sand source
    """
    grid = [['.' for i in range(w)] for j in range(h)]

    for r in rocks:
        grid[r.y][r.x] = '#'

    for s in sand:
        grid[s.y][s.x] = 'o'
    
    grid[sand_src.y][sand_src.x] = '+'

    for j in range(h):
        print("".join(grid[j]))
    print()

def point_is_rock_or_sand(point, rocks, sand):
    """
    Determines whether the specified point is on a rock (path) or existing sand
    """
    return (point in rocks) or (point in sand)


def part1(input):
    
    paths = [[Point(*list(map(int, m.strip().split(",")))) for m in l.strip().split("->")] for l in input if l]
    # Add a single path (sand source) at the beginning of the list
    paths.insert(0, [Point(500, 0)])

    # Normalize paths and compute width and height of the simulation grid
    sand_src, rocks, w, h = normalize_paths(paths)

    # Keep track of sand units
    sand = set([])
    
    # Draw initial state
    if DRAW_SIMULATION:
        draw_state(w, h, rocks, sand, sand_src)
    
    # As long as sand is moving inside the grid (check at the end of loop)
    while True:
        # Attempt to generate sand and move straight down from sand source
        curr_x, curr_y = sand_src.x, sand_src.y + 1
        can_move = not point_is_rock_or_sand(Point(curr_x, curr_y), rocks, sand)
        
        # As long as the newly generated sand can move (inside the grid)
        while can_move and 0 <= curr_x < w and 0 <= curr_y < h:
            # Attempt to move straight down
            curr_y += 1
            intersection = point_is_rock_or_sand(Point(curr_x, curr_y), rocks, sand)
            
            if intersection:
                # Intersected with sand or path
                # Attempt to fall left
                if not point_is_rock_or_sand(Point(curr_x - 1, curr_y), rocks, sand):
                    curr_x -= 1
                    can_move = True
                
                elif not point_is_rock_or_sand(Point(curr_x + 1, curr_y), rocks, sand):
                    # Attempt to fall right if left is blocked
                    curr_x += 1
                    can_move = True
                
                else:
                    # Stop on top if everything else failed
                    curr_y -= 1
                    can_move = False

        if curr_x < 0 or curr_x >= w or curr_y < 0 or curr_y >= h:
            # Last step was falling outside grid, stop
            break

        sand.add(Point(curr_x, curr_y))
        
        if DRAW_SIMULATION:
            draw_state(w, h, rocks, sand, sand_src)

    return len(sand)

def part2(input):
    return len(input)

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 24)
    # test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")