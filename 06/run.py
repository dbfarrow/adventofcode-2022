#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=6)

    # this method takes an array of input line because the test
    # data set has several messages in it. ultimately, for the 
    # real data, we only care about the first line in the input
    def get_start_of_packet(self, data, n):
        offsets = []
        for d in data:
            for i in range(len(d) - n):
                if len(set(d[i:i+n])) == n:
                    log.info(f'{(d[:80] + "...") if len(d) > 80 else d}: {i+n}')
                    offsets.append(i+n)
                    break
        return offsets[0]

    def A(self):
        return self.get_start_of_packet(self.get_input(), 4)

    def B(self):
        return self.get_start_of_packet(self.get_input(), 14)


if __name__ == "__main__":
    AOC().run()
