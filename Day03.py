import sys
import os

from Utils import *


prio = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def part1(input):
    total = 0

    for line in input:
        full_len = len(line)
        compA = line[0:full_len//2]
        compB = line[full_len//2:]
        setA = set(compA)
        setB = set(compB)
        incorrect = setA.intersection(setB)
        total += prio.index(incorrect.pop()) + 1

    return total

def part2(input):
    total = 0
    num_groups = len(input) // 3

    for g in range(0, num_groups):
        group = set.intersection(*[set(r.replace('\n', '')) for r in input[g*3:(g+1)*3]])
        total += prio.index(group.pop()) + 1

    return total

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 157)
    test_part(f"data/{filename}_test.txt", part2, 70)
    main(f"data/{filename}.txt")