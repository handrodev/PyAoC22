import sys
import os

from Utils import *


def part1(input):
    cycle = 1
    regval = 1
    signal_strengths = []

    for line in input:
        
        cycle += 1
        if (cycle - 20) % 40 == 0:
            signal_strengths.append(cycle * regval)
        if cycle >= 220:
            break
        
        if line.startswith("addx"):
            _, X = line.rstrip().split(" ")
            regval += int(X)
            cycle += 1
            
            if (cycle - 20) % 40 == 0:
                signal_strengths.append(cycle * regval)
            if cycle >= 220:
                break

    return sum(signal_strengths)

def part2(input):
    cycle = 1
    regval = 1

    CRT_W, CRT_H = (40, 6)
    CRT = [['.' for c in range(CRT_W)] for r in range(CRT_H)]
    row = 0
    col = 0

    if col in [regval - 1, regval, regval + 1]:
        CRT[row][col] = '#'

    for line in input:
        cycle += 1
        col += 1

        if col >= CRT_W:
            row += 1
            col = 0

        if cycle >= CRT_W * CRT_H:
            break

        if col in [regval - 1, regval, regval + 1]:
            CRT[row][col] = '#'
        
        if line.startswith("addx"):
            _, X = line.rstrip().split(" ")
            regval += int(X)
            cycle += 1
            col += 1

            if col >= CRT_W:
                row += 1
                col = 0
            
            if cycle >= CRT_W * CRT_H:
                break

            if col in [regval - 1, regval, regval + 1]:
                CRT[row][col] = '#'
    
    for r in CRT:
        print("".join(r))
    print()

    return 0

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    part2(lines)

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 13140)
    test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")