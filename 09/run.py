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
        return [ self.parse_input(l) for l in super().get_input() ]

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

#       log.info(f'move_head: {h} -> {m} -> ({x}, {y})')
        return (x, y)
 
    def is_adjacent(self, h, t):
        return (abs(h[0] - t[0]) <= 1) and (abs(h[1] - t[1]) <= 1)

    def move_tail(self, h, t):
        moves = []
        T = t
        while not self.is_adjacent(h, t):
            if (t[1] == h[1]) and (t[0] != h[0]):   # in the same row
                incr = 1 if h[0] > t[0] else -1
                t = (t[0] + incr, t[1])
            elif (t[1] != h[1]) and (t[0] == h[0]): # in the same column
                incr = 1 if h[1] > t[1] else -1
                t = (t[0], t[1] + incr) 
            else:                                   # gotta move diagonally
                x_incr = 1 if h[0] > t[0] else -1
                y_incr = 1 if h[1] > t[1] else -1
                t = (t[0] + x_incr, t[1] + y_incr)
            moves.append(t)

#       log.info(f'   move_tail: {T} - {h} -> {moves}')
        new_t = moves[-1] if len(moves) > 0 else t
        return moves, new_t 
        
    def A(self):
        h = t = (0, 0)
        head_moves = self.get_input()
        tail_moves = [[(0, 0)]]
        for m in head_moves:
            h = self.move_head(h, m)                
            moves, t = self.move_tail(h, t)
            tail_moves.append(moves)

        return len(set([ m for tm in tail_moves for m in tm ]))

    def B(self):
        return None

if __name__ == "__main__":
    AOC().run()
