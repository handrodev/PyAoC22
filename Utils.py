import sys
import traceback

def read_input(filename):
    try:
        with open(filename, "r") as f:
            result = f.readlines()
    except IOError as e:
        print(e, file=sys.stderr)
        return None
    except Exception as e:
        print(e, file=sys.stderr)
        return None

    return result

def test_part(filename, part_func, expected_result):
    try:
        test_res = part_func(read_input(filename))
        assert(test_res == expected_result)
    except AssertionError as e:
        print(test_res)
        traceback.print_exc()
