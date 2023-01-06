import sys
import os

from collections import namedtuple

from Utils import *

CHAMBER_WIDTH = 7

def inside_walls(rock: tuple[int,...]) -> bool:
    # If all cells of rock are within the walls
    if rock[0][0] >= 0 and rock[-1][0] < CHAMBER_WIDTH:
        return True
    return False

def check_collision(rock: tuple[int,...], occupied: set[tuple[int,...]]) -> bool:
    # Check all cells agains all other rocks
    for c in rock:
        if c in occupied:
            return True
    return False


def rock_generator(i: int, y: int) -> tuple[int,...]:
    rock_types = (
        # Minus (-) shaped rock
        ((2, y), (3, y), (4, y), (5, y)),
        # Plus (+) shaped rock
        ((2, y + 1), (3, y), (3, y + 1), (3, y + 2), (4, y + 1)),
        # L shaped rock
        ((2, y), (3, y), (4, y), (4, y + 1), (4, y + 2)),
        # Vertical (|) shaped rock
        ((2, y), (2, y + 1), (2, y + 2), (2, y + 3)),
        # Square shaped rock
        ((2, y), (2, y + 1), (3, y), (3, y + 1))
    )
    
    return rock_types[i % len(rock_types)]
        


def part1(input, max_rocks=2022):
    # Input is only one line in this case
    jets = input[0].strip()
    num_jets = len(jets)

    # Keep track of occupied cells
    # Start with floor: (x=0..CHAMBER_WIDTH, y=-1)
    occupied = set([(x, 0) for x in range(0, CHAMBER_WIDTH)])

    max_y = 0
    num_rocks = 0
    i = 0
    j = 0
    # Simulate until the required maximum number of rocks has been reached
    while num_rocks < max_rocks:
        # print("A new rock begins falling")
        
        # Spawn new rock 2 units from left wall and 3 units above highest rock
        r = rock_generator(i, max_y + 4)
        i = (i + 1) % 5

        # As long as rock can still move
        while True:
            # Attempt to move by jet push
            jet_move = 1 if jets[j] == '>' else -1
            j = (j + 1) % num_jets
            
            rx = tuple((x + jet_move, y) for x, y in r)
            
            # Collision detected, cannot move in that direction
            if not inside_walls(rx) or check_collision(rx, occupied):
                # Go back to previous position
                # print(f"Jet of gas pushes rock {'right' if jet_move == 1 else 'left'}, but nothing happens")
                rx = r
            # else:
                # print(f"Jet of gas pushes rock {'right' if jet_move == 1 else 'left'}")

            # Attempt to fall down 1 unit
            ry = tuple((x, y - 1) for x, y in rx)
            
            # Collision detected, cannot fall down further
            if check_collision(ry, occupied):
                # Go back to previous position and stop
                ry = rx
                
                # Since rock stopped, mark corresponding cells as occupied
                for c in ry:
                    occupied.add(c)
                
                # Update max_y
                r_max_y = max(y for x, y in ry)  # Max y for current rock
                max_y = max(max_y, r_max_y)
                # print("Rock falls 1 unit, causing it to come to rest")
                break
            else:
                r = ry
                # print("Rock falls 1 unit")

        num_rocks += 1

    return max_y


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
    test_part(f"data/{filename}_test.txt", part1, 3068)
    # test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")
