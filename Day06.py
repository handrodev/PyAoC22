import sys
import os

from Utils import *


def part1(input):
    # Input is only one line in this case
    input = input[0]
    marker_buffer = []

    for idx, char in enumerate(input):
        if len(marker_buffer) < 4:
            if char in marker_buffer:
                # Character is repeated
                # Remove first character until the repeated one
                found_at = marker_buffer.index(char)
                del marker_buffer[:found_at+1]
            marker_buffer.append(char)
        else:
            # Found four different characters
            return idx

    return -1

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
    
    test_part(f"data/{filename}_test.txt", part1, 10)
    # test_part(f"data/{filename}_test.txt", part2, 0)

    main(f"data/{filename}.txt")