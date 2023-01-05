import sys
import os
import re

from Utils import *
from itertools import permutations


def parse_input(input):
    """
    Parses the input data (valves, flowrates, children)
    and returns flowrate map, distances map and indices map
    """
    names_regex = re.compile("([A-Z]{2})")
    flowrate_regex = re.compile("flow rate=(\d+);")

    # Valves graph: <Key=Valve> -> <Value=Children>
    graph = {}
    # Flowrates map: <Key=Valve> -> <Value=Flowrate>
    flowrates = {}

    # Parse input
    for line in input:
        line = line.strip()
        # Find all valves in a single line
        names = names_regex.findall(line)
        # First is the current valve's name, the rest are its children
        valvename, children = names[0], names[1:]
        # Get the flowrate for the current valve
        flowrate = int(flowrate_regex.findall(line)[0])
        # Create graph of valves v. children
        graph[valvename] = children
        # And keep track of valves with flowrates > 0
        if flowrate > 0:
            flowrates[valvename] = flowrate

    # Compute distances for each pair of valves with Floyd-Warhsall
    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    distances = {(v, w): 1 if w in graph[v] else float('inf') for w in graph for v in graph}
    for k, i, j in permutations(graph, 3):
        distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])
    
    # Create a unique index for each valve with flowrate > 0
    # Valve 0 | Valve 1 | Valve 2 ... | Valve N
    #    1         2          4            2^N
    indices = {valve: 1 << i for i, valve in enumerate(flowrates)}

    return flowrates, distances, indices

def backtracking(valve, flowrates, distances, indices, minutes, bitmask, pressure, result):
        # Backtracking with bitmasks
        # https://towardsdatascience.com/understanding-bitmask-for-the-coding-interview-b1643f4b0e24#5e7e
        # Keep maximum pressure until now for this solution
        result[bitmask] = max(result.get(bitmask, 0), pressure)

        # For each valve with flowrate > 0
        for w, flow in flowrates.items():
            # Compute remaining time as previous time - walking distance (- 1 to open valve)
            remaining_minutes = minutes - distances[valve, w] - 1
            if not indices[w] & bitmask and remaining_minutes > 0:
                # Valve not visited yet and there is still time
                # Open and visit next valve
                backtracking(w, flowrates, distances, indices, remaining_minutes, bitmask | indices[w], pressure + flow * remaining_minutes, result)
        
        return result


def part1(input):
    # Parse input and get parsed data
    fr, dist, idx = parse_input(input)
    solutions = backtracking('AA', fr, dist, idx, 30, 0, 0, {})
    
    return max(solutions.values())

def part2(input):
    # Parse input and get parsed data
    fr, dist, idx = parse_input(input)
    solutions = backtracking('AA', fr, dist, idx, 26, 0, 0, {})
    
    # Return the best combination of solutions where 
    # elephant has visited different valves than me (not b1 & b2)
    return max(s1 + s2 for b1, s1 in solutions.items() for b2, s2 in solutions.items() if not b1 & b2)
    

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return

    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 1651)
    test_part(f"data/{filename}_test.txt", part2, 1707)
    main(f"data/{filename}.txt")