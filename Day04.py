import sys
import os

from Utils import *

def part1(input):
    problematic = 0

    for line in input:
        s1, s2 = line.replace("\n", "").split(",")
        sec1, sec2 = [s.split("-") for s in (s1, s2)]
        sec1 = list(map(int, sec1))
        sec2 = list(map(int, sec2))

        if (sec2[0] >= sec1[0] and sec2[1] <= sec1[1]) or \
            (sec1[0] >= sec2[0] and sec1[1] <= sec2[1]):
            # Check if one of the ranges
            # completely contains the other
            problematic += 1
        
    return problematic

def part2(input):
    problematic = 0

    for line in input:
        s1, s2 = line.replace("\n", "").split(",")
        sec1, sec2 = [s.split("-") for s in (s1, s2)]
        x1, x2 = list(map(int, sec1))
        y1, y2 = list(map(int, sec2))

        if (x1 <= y2 and y1 <= x2):
            # Check if ranges overlap
            problematic += 1 
        
    return problematic

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 2)
    test_part(f"data/{filename}_test.txt", part2, 4)
    main(f"data/{filename}.txt")