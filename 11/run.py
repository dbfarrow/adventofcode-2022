#!/usr/bin/env python3
import sys
sys.path.append('..')

from functools import reduce
import json
from math import floor
import re

from shared.aoc import __AOC
from shared import log

class Monkey:

    reduce_worry = True

    def __init__(self, block):

        self.inspected = 0

        # first line is the monkey id
        m = re.match('Monkey (\d+):', block[0])
        self.id = int(m.group(1))

        # the second is the list of items the monkey has and
        # my level of worry about it
        #   Starting items: 79, 98
        m = re.match('  Starting items: (.*)', block[1])
        self.items = list(map(int, m.group(1).split(',')))
        
        # the third is the operation to perform
        #   Operation: new = old * 19
        m = re.match('  Operation: new = old (.+) (.+)', block[2])
        self.operator = m.group(1)
        self.operand = int(m.group(2)) if m.group(2) != 'old' else m.group(2)
 
        #   Test: divisible by 23
        m = re.match('  Test: divisible by ([0-9]+)', block[3])
        self.test_divisor = int(m.group(1))

        #     If true: throw to monkey 2
        m = re.match('    If true: throw to monkey ([0-9]+)', block[4])
        self.test_true = int(m.group(1))

        #     If false: throw to monkey 3
        m = re.match('    If false: throw to monkey ([0-9]+)', block[5])
        self.test_false = int(m.group(1))

    def __repr__(self):
        return f'{self.id}: inspected: {self.inspected:4}; items: {self.items}'

    def operate(self, old):
        
        if self.operator == '+':
            return old + (old if self.operand == 'old' else self.operand)
        elif self.operator == '*':
            return old * (old if self.operand == 'old' else self.operand)
        else:
            raise Exception (f'unknown operator: {self.operator}')

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=11)

    def get_input(self):
        lines = super().get_input()
        return [ Monkey(lines[i:i+7]) for i in range(0, len(lines), 7) ]

    def play_round(self, monkeys, space):
        
        for mid in sorted(monkeys):
            m = monkeys[mid]
            for i in m.items:

                # reduce worry because the monkey's inspection didn't break the item
                # and compute the specified operation
                new = m.operate(i)
                if Monkey.reduce_worry:
                    new = floor(new/3)

                recip = m.test_true if new % m.test_divisor == 0 else m.test_false
                new = new % space
                monkeys[recip].items.append(new)
            m.inspected += len(m.items)
            m.items = []

        return

    def play(self, numrounds, reduce_worry):

        Monkey.reduce_worry = reduce_worry
        monkeys = { m.id: m for m in self.get_input() }
            
        # we can limit the max worry value by wrapping worry values at the product
        # of all the monkey's test divisor. i'd love to explain why. but i can't
        space = reduce(lambda x, y: x * y, [ m.test_divisor for m in monkeys.values() ])

        for r in range(numrounds):
            self.play_round(monkeys, space)

        activity = list(sorted([ m.inspected for m in monkeys.values() ]))
        return activity[-1] * activity[-2]

    def A(self):
        return self.play(20, True)

    def B(self):
        return self.play(10000, False)
        return None

if __name__ == "__main__":
    AOC().run()
