import sys
import os
from math import sqrt

from Utils import *

def draw_state(nodes, dimensions):
    num_nodes = len(nodes)
    result = [['.' for n in range(dimensions[1])] for m in range(dimensions[0])]

    # Tail has the lowest drawing prio
    result[nodes[-1][1]][nodes[-1][0]] = "T"

    # Then all the nodes from 1 to num_nodes - 1
    for n in range(1, num_nodes - 1):
        # But only if empty or tail
        if result[nodes[n][1]][nodes[n][0]] in [".", "T"]:
            result[nodes[n][1]][nodes[n][0]] = str(n)

    # Head hast the highest prio
    # overwrite anything previously drawn
    result[nodes[0][1]][nodes[0][0]] = "H"
    
    for r in reversed(result):
        print("".join(r))
    
    print("\n")


def next_state(nodes_pos, dir, moves, unique_tail, draw_states=False, dimensions=(5,6)):
    """
    Computes the next state of the chain given the current state (nodes_pos)
    the direction of movement and the number of movements in that direction.
    
    Returns the current state and the set of unique positions visited bz tail until now
    """
    chain_len = len(nodes_pos) 
    # Relative positions of each of the rope nodes, all start overlapping
    # Head position is nodes_pos[0], position of tail is nodes_pos[-1]
    for m in range(0, moves):
        # Move head first
        if dir == "R":
            # Right
            nodes_pos[0][0] += 1
        elif dir == "U":
            # Up
            nodes_pos[0][1] += 1
        elif dir == "L":
            # Left
            nodes_pos[0][0] -= 1
        elif dir == "D":
            # Down
            nodes_pos[0][1] -= 1

        for n in range(1, chain_len):
            h_offset = nodes_pos[n-1][0] - nodes_pos[n][0]
            v_offset = nodes_pos[n-1][1] - nodes_pos[n][1]
            
            if abs(h_offset) == 1:
                if abs(v_offset) == 1:
                    pass  # Adjacent diagonally, do nothing
                elif v_offset == +2:
                    nodes_pos[n] = [nodes_pos[n-1][0], nodes_pos[n][1] + 1]
                elif v_offset == -2:
                    nodes_pos[n] = [nodes_pos[n-1][0], nodes_pos[n][1] - 1]
            elif h_offset == +2:
                nodes_pos[n][0] += 1
                if abs(v_offset) == 1:
                    nodes_pos[n][1] = nodes_pos[n-1][1]
                elif v_offset == +2:
                    nodes_pos[n][1] += 1
                elif v_offset == -2:
                    nodes_pos[n][1] -= 1
            elif h_offset == -2:
                nodes_pos[n][0] -= 1
                if abs(v_offset) == 1:
                    nodes_pos[n][1] = nodes_pos[n-1][1]
                elif v_offset == +2:
                    nodes_pos[n][1] += 1
                elif v_offset == -2:
                    nodes_pos[n][1] -= 1
            elif h_offset == 0:
                if v_offset == 2:
                    nodes_pos[n][1] += 1
                elif v_offset == -2:
                    nodes_pos[n][1] -= 1
        
        if draw_states:
            draw_state(nodes_pos, dimensions)

        unique_tail.add(tuple(nodes_pos[-1]))

    return nodes_pos, unique_tail


def solution(input, chain_length=2, draw_states=False, dimensions=(5,6)):
    nodes_pos = [[0, 0] for n in range(chain_length)]
    tail_visited = {tuple(nodes_pos[-1])}  # Cells visited by tail (last rope node node[-1])

    if draw_states:
        # Draw initial state if specified
        print("== Initial State ==\n")
        draw_state(nodes_pos, dimensions)

    for line in input:
        # Get direction and number of moves in that direction
        head_dir, moves = line.strip().split(" ")
        moves = int(moves)
        
        if draw_states:
            # Log current move
            print(f"== {head_dir} {moves} ==\n")

        # Compute the next state
        nodes_pos, tail_visited = next_state(nodes_pos, head_dir, moves, tail_visited, draw_states, dimensions)
    
    return len(tail_visited)

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(solution(lines, 2, False))
    print(solution(lines, 10, False))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    # test_part(f"data/{filename}_test.txt", lambda x: solution(x, 2, True, (5, 6)), 13)
    # test_part(f"data/{filename}_test.txt", lambda x: solution(x, 10, True, (5, 6)), 1)
    main(f"data/{filename}.txt")