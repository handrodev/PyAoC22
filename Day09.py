import sys
import os
from math import sqrt

from Utils import *


def part1(input):
    head_pos = (0, 0)  # Relative position of head
    tail_pos = (0, 0)  # Relative position of tail (initially overlapping)
    tail_visited = {tail_pos}  # Cells visited by tail
    dist = 0.0  # Distance between head and tail

    for line in input:
        head_dir, moves = line.strip().split(" ")
        moves = int(moves)
        
        for m in range(1, moves+1):
            # Move head first
            if head_dir == "R":
                # Right
                head_pos = (head_pos[0] + 1, head_pos[1])
            elif head_dir == "U":
                # Up
                head_pos = (head_pos[0], head_pos[1] + 1)
            elif head_dir == "L":
                # Left
                head_pos = (head_pos[0] - 1, head_pos[1])
            elif head_dir == "D":
                # Down
                head_pos = (head_pos[0], head_pos[1] - 1)

            # Compute euclidean distance between head and tail
            dist = sqrt(pow(head_pos[1] - tail_pos[1], 2) + pow(head_pos[0] - tail_pos[0], 2))

            if dist > sqrt(2.0):
                if head_dir == "R":
                    tail_pos = (tail_pos[0] + 1, tail_pos[1])
                elif head_dir == "U":
                    tail_pos = (tail_pos[0], tail_pos[1] + 1)
                elif head_dir == "L":
                    tail_pos = (tail_pos[0] - 1, tail_pos[1])
                elif head_dir == "D":
                    tail_pos = (tail_pos[0], tail_pos[1] - 1)
                
                # If the tail is diagonally offset from the head
                # snap it depending on previous head's movement direction
                if (abs(tail_pos[0] - head_pos[0]) >= 1 and abs(tail_pos[1] - head_pos[1]) >=1):
                    if head_dir in ["U", "D"]:
                        tail_pos = (head_pos[0], tail_pos[1])
                    elif head_dir in ["L", "R"]:
                        tail_pos = (tail_pos[0], head_pos[1])

                tail_visited.add(tail_pos)
    
    return len(tail_visited)

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
    test_part(f"data/{filename}_test.txt", part1, 13)
    # test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")