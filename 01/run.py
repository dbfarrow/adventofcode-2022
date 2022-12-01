#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=1) # <----- fill in day here

    def compute_totals(self):
        totals = []
        total = 0
        for i in self.get_input():
            try:
                total += int(i)
            except:
                # we get here because a blank line won't cast to an int. so it must
                # be a break between elves. save the current elf's total and reset
                # for the next elf
                totals.append(total)
                total = 0
    
        # don't forget the last elf
        totals.append(total)
        return totals
 
    def A(self):
        totals = self.compute_totals()
        return max(totals)

    def B(self):
        totals = self.compute_totals()
        totals.sort(reverse=True)
        return sum(totals[0:3])

if __name__ == "__main__":
    AOC().run()
