import sys
import os
from queue import PriorityQueue

from Utils import *

def char_dist(char_1, char_2):
    # Replace S -> a and E -> z since distance in those cases shall be 0
    char_1 = char_1.replace('E', 'z').replace('S', 'a')
    char_2 = char_2.replace('E', 'z').replace('S', 'a')
    # Compares two characters and returns the distance
    return ord(char_1) - ord(char_2)

def next_moves(input_grid, curr_pos):
    row, col = curr_pos
    curr_char = input_grid[row][col]
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # LURD
    neighbors = set([
        # Left
        (row,                        max(0, col - 1)),
        # Up
        (max(0, row - 1),            col),
        # Right
        (row,                        min(num_cols - 1, col + 1)),
        # Down
        (min(num_rows - 1, row + 1), col)
    ])

    # Leave only valid moves, elevation_change <= 1
    return list(filter(lambda pos: char_dist(input_grid[pos[0]][pos[1]], curr_char) <= 1, neighbors))
    
def find_cells(input, values):
    return [(i, j) for i, row in enumerate(input) for j, col in enumerate(row) if input[i][j] in values]

def part1(input, source=None):
    for r in range(len(input)):
        input[r] = input[r].strip()  # Remove \n for each line in input
    
    if source is None:
        source = find_cells(input, ['S'])[0]
    target = find_cells(input, ['E'])[0]

    # Start with a long path where each cell is visited
    # since no path can be longer than that, this is our "infinity" length
    infinity = len(input) * len(input[0])

    # Solve path using modified dijsktra algorithm between source and target
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    # For each vertex V in Graph (input)
    
    # Array with distance from source to each other vertex
    dist_v = {(r, c): infinity for r in range(len(input)) for c in range(len(input[0]))}
    dist_v[source] = 0
    prev_v = {(r, c): None for r in range(len(input)) for c in range(len(input[0]))}

    pq = PriorityQueue()
    pq.put((0, source))

    while not pq.empty():
        (dist, current_vertex) = pq.get()

        if current_vertex not in dist_v:
            dist_v[current_vertex] = infinity

        for neighbor in next_moves(input, current_vertex):
            if neighbor not in dist_v:
                dist_v[neighbor] = infinity
            new_cost = dist_v[current_vertex] + 1

            if new_cost < dist_v[neighbor]:
                pq.put((new_cost, neighbor))
                dist_v[neighbor] = new_cost
                prev_v[neighbor] = current_vertex
    
    S = []
    u = target
    if prev_v[u] is not None or u == source:
        while u is not None:
            S.append(u)
            u = prev_v[u]
    
    return dist_v[target]


def part2(input):
    return min([part1(input, start) for start in find_cells(input, ['S', 'a'])])

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 31)
    test_part(f"data/{filename}_test.txt", part2, 29)
    main(f"data/{filename}.txt")