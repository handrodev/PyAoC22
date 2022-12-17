import sys
import os

from Utils import *

import numpy as np

def get_elves_calories(input):
    input = np.array([l.replace("\n", "") for l in input])
    input[input == ''] = 0
    input = input.astype(np.int64)
    return [sum(elf) for elf in np.split(input, np.where(input == 0)[0])]

def part1(input):
    elves = get_elves_calories(input)
    return max(elves)

def part2(input):
    elves = get_elves_calories(input)
    return sum(sorted(elves)[-3:])

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    # test_part(f"data/{filename}_test.txt", part1, 2)
    # test_part(f"data/{filename}_test.txt", part2, 4)
    main(f"data/{filename}.txt")