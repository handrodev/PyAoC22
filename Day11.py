import sys
import os
import re
from operator import mul
from functools import reduce

from Utils import *


class Monkey:
    def __init__(self, items, operator, operand, div_test, div_true, div_false, divide_by_3=True):
        self.items = items
        self.operand = operand
        self.operator = operator
        self.div_test = div_test
        self.div_true = div_true
        self.div_false = div_false
        self.inspected_items = 0
        self.divide_by_3 = divide_by_3
    
    def inspect(self, divide_by_3=True):
        result = []
        self.inspected_items += len(self.items)

        while len(self.items) > 0:
            obj = self.items.pop(0)

            if self.operand == 'old':
                operand_val = obj
            else:
                operand_val = int(self.operand)

            if self.operator == '*':
                obj *= operand_val
            elif self.operator == '+':
                obj += operand_val
            
            if self.divide_by_3:
                obj //= 3
            result.append((obj, self.test(obj)))
        
        return result

    def test(self, obj):
        if obj % self.div_test == 0:
            return self.div_true
        
        return self.div_false

def solution(input, rounds=20, divide_by_3=True):
    monkeys = []
    items_regex = re.compile("(\d+)(?:,\s*)?")
    op_regex = re.compile("\s*Operation: new = old ([\*\+]) (\d+|old)")

    # Parse input, get monkeys and create list of monkey objects
    # With corresponding operations
    input = list(filter(lambda x: x != "\n" and x != '', input))
    input = [l.strip() for l in input]
    num_monkeys = len(input) // 6

    for i in range(num_monkeys):
        monkey_input = input[i*6:(i+1)*6]
        
        items = list(map(int, items_regex.findall(monkey_input[1])))
        operator, operand = op_regex.match(monkey_input[2]).groups()

        div_test = int(monkey_input[3].split()[-1])
        div_true = int(monkey_input[4].split()[-1])
        div_false = int(monkey_input[5].split()[-1])

        monkeys.append(Monkey(items, operator, operand, div_test, div_true, div_false, divide_by_3))

    # Start simulation for as many rounds as required
    for c in range(rounds):
        for m in range(num_monkeys):
            result = monkeys[m].inspect()
        
            for item in result:
                obj, to_monkey = item[0], item[1]
                monkeys[to_monkey].items.append(obj)
        
        # print(f"After round {c+1}:")
        # for idx, m in enumerate(monkeys):
        #     print(f"Monkey {idx}: {m.items}")
        # print()

    return reduce(mul, list(sorted([m.inspected_items for m in monkeys], reverse=True))[0:2])

def main(input):
    lines = read_input(input)

    if lines is None:
        print("Error reading input!")
        return
    
    print(solution(lines, 20, True))
    print(solution(lines, 1000, False))

if __name__ == "__main__":
    filename = os.path.splitext(sys.argv[0])[0]
    # test_part(f"data/{filename}_test.txt", lambda x: solution(x, 20, True), 10605)
    test_part(f"data/{filename}_test.txt", lambda x: solution(x, 10000, False), 2713310158)
    # main(f"data/{filename}.txt")