import sys
import os
import re
from collections import deque

from Utils import *

def parse_input(input):
    # Parses the input and returns the stacks as a list of strings
    # And the moves as a list of 3-tuples (crates being moved, source stack, target stack)
    stacks_regex = re.compile(r"( ? {3} ?| ?[A-Z] ?)")
    moves_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")

    moves = []
    stack_matches = []
    for line in input:
        # Process input, get initial stacks
        stack_match = stacks_regex.findall(line)
        if len(stack_match) > 0:
            stack_matches.append(stack_match)
        # Get moves
        moves_matches = moves_regex.match(line)
        if moves_matches is not None:
            moves.append(tuple(map(int, moves_matches.groups())))

    # Reverse stacks so they are built from top to bottom
    stack_matches.reverse()
    # Remove first (last) row, which are just the numbers for each column
    del stack_matches[0]

    # Transpose list so we get each stack
    stacks = []
    for z in zip(*stack_matches):
        # Treat stacks as strings from left to right (bottom to top)
        stack = "".join(z).replace(" ", "")
        stacks.append(stack)

    return (stacks, moves)

def part1(input):
    stacks, moves = parse_input(input)

    for times, source, target in moves:
        # Moving crates one at a time reverses the original order at source
        # So append (stack) crates in reverse order at the top of target stack
        stacks[target-1] += stacks[source-1][:-times-1:-1]
        # Remove last "times" elements from source stack
        stacks[source-1] = stacks[source-1][:-times]

    # Result is the last char (top crate) of each stack
    return "".join([s[-1] for s in stacks])

def part2(input):
    stacks, moves = parse_input(input)

    for crates, source, target in moves:
        # Moving crates all at the same time does NOT reverse the original order at source
        # So append (stack) crates in original order at the top of target stack
        stacks[target-1] += stacks[source-1][-crates:]
        # Remove crates source stack
        stacks[source-1] = stacks[source-1][:-crates]

    # Result is the last char (top crate) of each stack
    return "".join([s[-1] for s in stacks])

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, "CMZ")
    test_part(f"data/{filename}_test.txt", part2, "MCD")
    main(f"data/{filename}.txt")