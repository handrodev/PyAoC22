import sys
import os

from Utils import *


def part1(input):
    return len(input)

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
    test_part(f"data/{filename}_test.txt", part1, 0)
    test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")