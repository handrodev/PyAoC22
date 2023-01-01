import sys
import os

from Utils import *


def part1(input):
    correct_indices = []
    pair_index = 1
    left = None
    right = None

    def compare_elements(left, right):
        # print(f"Compare {left} and {right}")
        
        if isinstance(left, int) and isinstance(right, int):
            if left > right:
                # print(f"Left {left} > right {right}: incorrect order")
                return -1
            elif left < right:
                # print(f"Left {left} < right {right}: right order")
                return 1
            else:
                # print(f"Left {left} == right {right}: continue")
                return 0

        elif isinstance(left, list) and isinstance(right, list):
            result = 0
            n = len(left)
            m = len(right)
            for i in range(min(n, m)):
                result = compare_elements(left[i], right[i])
                if result:
                    break
            if result == 0:
                if n < m:
                    # print(f"Left ran out of items before right did: right order")
                    return 1
                elif n > m:
                    # print(f"Right ran out of items before left did: incorrect order")
                    return -1
                else:
                    # print(f"Same length, could not determine order: continue")
                    return 0

        elif isinstance(left, int):
            # print(f"Mixed types: converting {left} to {[left]}")
            result = compare_elements([left], right)

        elif isinstance(right, int):
            # print(f"Mixed types: converting {right} to {[right]}")
            result = compare_elements(left, [right])

        return result

    for line in input:
        line = line.strip()

        if line:  # Non-empty line
            if left is None:
                left = eval(line)
            elif right is None:
                right = eval(line)
            
            if left is not None and right is not None:
                # Got a pair of packets
                # Compare them
                # print("==================")
                # print(f"Pair {pair_index}")
                if compare_elements(left, right) == 1:
                   correct_indices.append(pair_index)
                # print()
                # Clear flags
                left = right = None
                # Increase pair index
                pair_index += 1

    # print(correct_indices)

    return sum(correct_indices)

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
    test_part(f"data/{filename}_test.txt", part1, 13)
    # test_part(f"data/{filename}_test.txt", part2, 0)
    main(f"data/{filename}.txt")