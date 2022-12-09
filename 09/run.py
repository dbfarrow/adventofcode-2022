#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=9)

    def parse_input(self, l):
        parts = l.split(' ')
        return (parts[0], int(parts[1]))

    def get_input(self):
        return [ self.parse_input(l) for l in super().get_input() if l[0] != '#' ]

    def move_head(self, h, m):
        x, y = h
        dir, dist = m
        if dir == 'U':
            y += dist
        elif dir == 'D':
            y -= dist
        elif dir == 'L':
            x -= dist
        elif dir == 'R':
            x += dist
        else:
            raise Exception(f'unknown dir: {dir}')

        return (x, y)
 
    def is_adjacent(self, h, t):
        return (abs(h[0] - t[0]) <= 1) and (abs(h[1] - t[1]) <= 1)

    def move(self, a, b):
        if (b[1] == a[1]) and (b[0] != a[0]):   # in the same row
            incr = 1 if a[0] > b[0] else -1
            return (b[0] + incr, b[1])
        elif (b[1] != a[1]) and (b[0] == a[0]): # in the same column
            incr = 1 if a[1] > b[1] else -1
            return (b[0], b[1] + incr) 
        else:                                   # gotta move diagonally
            x_incr = 1 if a[0] > b[0] else -1
            y_incr = 1 if a[1] > b[1] else -1
            return (b[0] + x_incr, b[1] + y_incr)
        
    def move_rope(self, num_knots):

        knots = [ (0,0) for i in range(num_knots) ]
        places = set([])
        for move in self.get_input():
            newhead = self.move_head(knots[0], move)
            while (knots[0] != newhead):
                for i in range(len(knots)):
                    if i == 0:
                        knots[i] = self.move(newhead, knots[i])
                    elif not self.is_adjacent(knots[i-1], knots[i]): 
                        knots[i] = self.move(knots[i-1] if i > 0 else newhead, knots[i])
                places.add(knots[-1])

        return len(places)

    def A(self):
        return self.move_rope(2)

    def B(self):
        return self.move_rope(10)

if __name__ == "__main__":
    AOC().run()
