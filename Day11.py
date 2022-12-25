import sys
import os
import re
from operator import mul
from functools import reduce

from Utils import *


class Monkey:
    def __init__(self, items, operation, div_test, div_true, div_false):
        self.items = items
        self.operation = lambda old: eval(operation)
        self.div_test = div_test
        self.div_true = div_true
        self.div_false = div_false
        self.inspected_items = 0

    def test(self, value):
        if value % self.div_test == 0:
            return self.div_true

        return self.div_false

def solution(input, rounds=20, divide_by_three=True):
    monkeys = {}
    items_regex = re.compile("(\d+)(?:,\s*)?")
    op_regex = re.compile("\s*Operation: new = (.*)")

    # Parse input, get monkeys and create list of monkey objects
    # With corresponding operations
    input = list(filter(lambda x: x != "\n" and x != '', input))
    input = [l.strip() for l in input]
    num_monkeys = len(input) // 6

    for i in range(num_monkeys):
        monkey_input = input[i*6:(i+1)*6]
        
        items = list(map(int, items_regex.findall(monkey_input[1])))
        operation = op_regex.match(monkey_input[2]).group(1)

        div_test = int(monkey_input[3].split()[-1])
        div_true = int(monkey_input[4].split()[-1])
        div_false = int(monkey_input[5].split()[-1])

        monkeys[i] = Monkey(items, operation, div_test, div_true, div_false)

    # Compute product of all monkey divisors
    divisor = reduce(mul, [m.div_test for m in monkeys.values()], 1)

    # Start simulation for as many rounds as required
    for r in range(rounds):
        for m in monkeys.values():
            curr_items = m.items
            m.inspected_items += len(curr_items)

            for item in curr_items:
                new_item = m.operation(item)
                if divide_by_three:
                    new_item //= 3
                new_item %= divisor

                target_monkey = m.test(new_item)
                monkeys[target_monkey].items.append(new_item)

            m.items = []

    return reduce(mul, list(sorted([m.inspected_items for m in monkeys.values()], reverse=True))[0:2], 1)

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(solution(lines, 20, True))
    print(solution(lines, 10000, False))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    test_part(f"data/{filename}_test.txt", lambda x: solution(x, 20, True), 10605)
    test_part(f"data/{filename}_test.txt", lambda x: solution(x, 10000, False), 2713310158)
    main(f"data/{filename}.txt")