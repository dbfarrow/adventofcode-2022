#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=4) 

    def get_input(self):
        lines = super().get_input()
        data = []
        for l in super().get_input():
            pairs = l.split(',')
            data.append((
                [int(x) for x in pairs[0].split('-')], 
                [int(x) for x in pairs[1].split('-')]
            ))
        return data

    def overlaps_completely(self, a, b):
        return max(a[1], b[1]) - min(a[0], b[0]) == max((a[1]-a[0]), (b[1]-b[0]))

    def overlaps_partially(self, a, b):
        return (b[0] <= a[0] <= b[1]) or (b[0] <= a[1] <= b[1]) or self.overlaps_completely(a, b)

    def A(self):
        return sum([ self.overlaps_completely(pair[0], pair[1]) for pair in self.get_input() ])

    def B(self):
        return sum([ self.overlaps_partially(pair[0], pair[1]) for pair in self.get_input() ])

if __name__ == "__main__":
    AOC().run()
