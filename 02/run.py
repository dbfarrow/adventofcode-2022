#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=2)

    def A(self):
        lookup = {
            'A X': (1 + 3),   # rock:rock = draw
            'A Y': (2 + 6),   # rock:paper = win
            'A Z': (3 + 0),   # rock:scissors = loss
            'B X': (1 + 0),   # paper:rock = loss
            'B Y': (2 + 3),   # paper:paper = draw
            'B Z': (3 + 6),   # paper:scissors = win
            'C X': (1 + 6),   # scissors:rock = win
            'C Y': (2 + 0),   # scissors:paper = loss
            'C Z': (3 + 3)    # scissors:scissors = draw
        }
        return sum([ lookup[p] for p in self.get_input() ])

    def B(self):
        lookup = {
            # choose to lose. the first number in the pair is
            # the value of your choice, the second is the value of the loss
            'A X': (3 + 0),   # rock:scissors = loss
            'B X': (1 + 0),   # paper:rock = loss
            'C X': (2 + 0),   # scissors:paper = loss

            # choose to draw. the first number in the pair is
            # the value of your choice, the second is the value of the draw
            'A Y': (1 + 3),   # rock:rock = draw
            'B Y': (2 + 3),   # paper:paper = draw
            'C Y': (3 + 3),   # scissors:scissors = draw

            # choose to win. the first number in the pair is
            # the value of your choice, the second is the value of the win
            'A Z': (2 + 6),   # rock:paper = win
            'B Z': (3 + 6),   # paper:scissors = win
            'C Z': (1 + 6)    # scissors:rock = win
        }
        
        return sum([ lookup[p] for p in self.get_input() ])

if __name__ == "__main__":
    AOC().run()
