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
    # Relative positions of each of the rope nodes, all start overlapping
    # Head position is nodes_pos[0], position of tail is nodes_pos[-1]
    CHAIN_LENGTH = 10
    nodes_pos = [(0, 0)] * CHAIN_LENGTH
    tail_visited = {nodes_pos[-1]}  # Cells visited by tail (last rope node node[-1])
    distances = [0.0] * (CHAIN_LENGTH - 1)  # Distance between each pair of nodes head -> 1, 1 -> 2, ... 8 -> 9

    for line in input:
        head_dir, moves = line.strip().split(" ")
        moves = int(moves)
        
        for m in range(1, moves+1):
            # Move head first
            if head_dir == "R":
                # Right
                nodes_pos[0] = (nodes_pos[0][0] + 1, nodes_pos[0][1])
            elif head_dir == "U":
                # Up
                nodes_pos[0] = (nodes_pos[0][0], nodes_pos[0][1] + 1)
            elif head_dir == "L":
                # Left
                nodes_pos[0] = (nodes_pos[0][0] - 1, nodes_pos[0][1])
            elif head_dir == "D":
                # Down
                nodes_pos[0] = (nodes_pos[0][0], nodes_pos[0][1] - 1)

            # Compute euclidean distance between each pair of nodes
            distances = [sqrt(
                pow(nodes_pos[n][1] - nodes_pos[n+1][1], 2) +
                pow(nodes_pos[n][0] - nodes_pos[n+1][0], 2)) for n in range(0, CHAIN_LENGTH - 1)
            ]

            # Update each node after head, following rules from part 1 for each pair of nodes
            for n in range(0, CHAIN_LENGTH - 1):
                if distances[n] > sqrt(2.0):
                    if head_dir == "R":
                        nodes_pos[n] = (nodes_pos[n][0] + 1, nodes_pos[n][1])
                    elif head_dir == "U":
                        nodes_pos[n] = (nodes_pos[n][0],     nodes_pos[n][1] + 1)
                    elif head_dir == "L":
                        nodes_pos[n] = (nodes_pos[n][0] - 1, nodes_pos[n][1])
                    elif head_dir == "D":
                        nodes_pos[n] = (nodes_pos[n][0],     nodes_pos[n][1] - 1)
                
                # If a node is diagonally offset from the one in front of it
                # snap it depending on previous head's movement direction
                if (abs(nodes_pos[n+1][0] - nodes_pos[n][0]) >= 1 and 
                    abs(nodes_pos[n+1][1] - nodes_pos[n][1]) >=1):
                    if head_dir in ["U", "D"]:
                        nodes_pos[n+1] = (nodes_pos[n][0], nodes_pos[n+1][1])
                    elif head_dir in ["L", "R"]:
                        nodes_pos[n+1] = (nodes_pos[n+1][0], nodes_pos[n][1])

                tail_visited.add(nodes_pos[-1])
    
    return len(tail_visited)

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