import sys
import os

from Utils import *


ABC2score = { "A": 1, "B": 2, "C": 3 }

def part1(input):
    # Rock = A / X, Paper = B / Y, Scissors = C / Z
    # A < B < C < A  
    XYZ2ABC = { "X": "A", "Y": "B", "Z": "C" }

    total_score = 0
    for line in input:
        playerB, playerA = line.split()
        # Add score corresponding to move
        playerA = XYZ2ABC[playerA]
        total_score += ABC2score[playerA]

        # Add score corresponding to result of match
        if (playerA == playerB):
            # Draw, add score 3
            total_score += 3
        else:
            if any([
                # Paper > Rock
                playerA == "B" and playerB == "A",
                # Scissors > Paper
                playerA == "C" and playerB == "B",
                # Rock > Scissors
                playerA == "A" and playerB == "C",
            ]):
                # Cases I (playerA) WIN
                total_score += 6
            else:
                # Cases I (playerA) LOSE
                # Do nothing: 0 score
                continue

    return total_score

def part2(input):
    total_score = 0
    result2ABC = {
        "A": {"X": "C", "Y": "A", "Z": "B"},
        "B": {"X": "A", "Y": "B", "Z": "C"},
        "C": {"X": "B", "Y": "C", "Z": "A"}
    }
    XYZ2score = {"X": 0, "Y": 3, "Z": 6}
    
    total_score = 0
    for line in input:
        playerB, result = line.split()
        # Now X,Y,Z are the results:
        # X = lose, Y = draw, Z = win
        playerA = result2ABC[playerB][result]
        total_score += ABC2score[playerA] + XYZ2score[result]

    return total_score

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 15)
    test_part(f"data/{filename}_test.txt", part2, 12)
    main(f"data/{filename}.txt")