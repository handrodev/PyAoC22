import sys
import os

import numpy as np

from Utils import *


def part1(input):
    # Create matrix from input
    input_m = np.asarray([[int(c) for c in line.strip()] for line in input], dtype='uint8')

    # Visible = 1, Hidden = 0
    visible_m = np.ones(input_m.shape)
    
    for r in range(1, input_m.shape[0]-1):
        for c in range(1, input_m.shape[1]-1):
            tree_h = input_m[r,c]
            # If all *other* trees in the row or column are larger or equal
            if all([np.any(input_m[r+1:,c] >= tree_h),
                    np.any(input_m[:r, c] >= tree_h),
                    np.any(input_m[r,:c] >= tree_h),
                    np.any(input_m[r, c+1:] >= tree_h)]):
                # The current tree is hidden
                visible_m[r, c] = 0

    # Count all visible trees by adding up both axis
    return np.sum(visible_m, axis=None, dtype='int64')

def part2(input):
    # Create matrix from input
    input_m = np.asarray([[int(c) for c in line.strip()] for line in input], dtype='uint8')
    score_m = np.zeros(input_m.shape, dtype="int64")

    for r in range(1, input_m.shape[0]-1):
        for c in range(1, input_m.shape[1]-1):
            tree_h = input_m[r,c]
            # Compute maximum viewing distance in each direction for current tree
            # Horizontal left
            taller_hl = np.nonzero(input_m[r, :c] >= tree_h)
            dist_hl = c - max(taller_hl[0]) if len(taller_hl[0]) > 0 else c
            
            # Horizontal right
            taller_hr = np.nonzero(input_m[r, c+1:] >= tree_h)
            # (c+1) + found_index - c
            dist_hr = min(taller_hr[0]) + 1 if len(taller_hr[0]) > 0 else input_m.shape[1] - 1 - c
            
            # Vertical top
            taller_vt = np.nonzero(input_m[:r, c] >= tree_h)
            dist_vt = r - max(taller_vt[0]) if len(taller_vt[0]) > 0 else r
            
            # Vertical bottom
            taller_vb = np.nonzero(input_m[r+1:, c] >= tree_h)
            # (r+1) + found_index - r
            dist_vb = min(taller_vb[0]) + 1 if len(taller_vb[0]) > 0 else input_m.shape[0] - 1 - r
            
            score_m[r, c] = dist_hl * dist_hr * dist_vt * dist_vb

    # Count all visible trees by adding up both axis
    # print(np.argmax(score_m))
    return np.max(score_m)

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(part1(lines))
    print(part2(lines))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", part1, 21)
    test_part(f"data/{filename}_test.txt", part2, 8)
    main(f"data/{filename}.txt")