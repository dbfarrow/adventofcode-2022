#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=3)

    def item_to_priority(self, item):
        return ord(item) - ord('A') + 27 if item.isupper() else ord(item) - ord('a') + 1

    def find_common_in_sack(self, contents):
        a, b = set(contents[0:len(contents)//2]), set(contents[len(contents)//2:])
        return self.item_to_priority(list(a.intersection(b))[0])
    
    def find_common_across_sacks(self, sacks):
        common = set(sacks[0])
        for j in range(1, len(sacks)):
            common = common.intersection(set(sacks[j]))
        return self.item_to_priority(list(common)[0])

    def A(self):
        return sum([ self.find_common_in_sack(contents) for contents in self.get_input() ])

    def B(self):
        sacks = self.get_input()
        groupsize = 3
        return sum([ self.find_common_across_sacks(sacks[i:i+groupsize]) for i in range(0, len(sacks), groupsize) ])

if __name__ == "__main__":
    AOC().run()
