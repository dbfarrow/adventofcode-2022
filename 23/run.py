#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from shared.aoc import __AOC
from shared import log

class Map:

    def __init__(self, data):

        self.map = defaultdict(list)
        self.max_y = len(data)
        self.max_x = len(data[0])

        pad = 70
        for i in range(pad):
            self.map[i].extend(list('.' * ((2 * pad) + self.max_x)))

        for y, r in enumerate(data):
            y += pad
            self.map[y].extend('.' * pad)
            for x, v in enumerate(r):
                self.map[y].extend(v)
            self.map[y].extend('.' * pad)

        for i in range(pad):
            self.map[i + y + 1].extend(list('.' * ((2 * pad) + self.max_x)))

    def get_bounds(self):

        min_x = min_y = 1024 * 1024 * 1024
        max_x = max_y = -min_x

        for y, r in self.map.items():
            if '#' in r:
                min_y = min(min_y, y)
                max_y = max(max_y, y)

            for x, v in enumerate(r):
                if v == '#':
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)

        return ((min_x, min_y), (max_x + 1, max_y + 1))

    def display(self):
        for y, r in self.map.items():
            log.info(f'{y:02}: {"".join(r)}')
        log.info('')


class AOC(__AOC):

    def __init__(self):
        super().__init__(day=23)
        self.dirs = [ 
            [ (-1, -1), (0, -1), (1, -1) ],     # north
            [ (-1, 1), (0, 1), (1, 1) ],        # south
            [ (-1, -1), (-1, 0), (-1, 1) ],     # west
            [ (1, -1), (1, 0), (1, 1) ],        # east
        ]


    def get_input(self):
        lines = [ l for l in super().get_input() if l[0] != ';' ]
        return Map(lines)
 
    def vote(self, mapp, turn):

        ends = defaultdict(list)

        for y, r in mapp.map.items():
            for x, v in enumerate(r):
                if mapp.map[y][x] == '.': continue      # not an elf
                start = (x, y)
                log.debug(f'voting for {start}: {mapp.map[y][x]}')

                possible_moves = []
                for i in range(4):
                    dirs = self.dirs[(turn + i) % 4]
                    neighbors = [ v for v in [ mapp.map[y + d[1]][x + d[0]] for d in dirs ] if v == '#' ]
                    log.debug(f'turn: {turn}; start: {start}; dirs: {dirs}; neighbors: {neighbors}')
                    if not any(neighbors):
                        possible_moves.append((x + dirs[1][0], y + dirs[1][1]))
                    else:
                        possible_moves.append(None)
    
                log.debug(f'possible moves for {start}: {possible_moves}')
                if all(possible_moves):
                    log.debug(f'freeze at {start} mofo!')
                elif not any(possible_moves):
                    log.debug(f'{start} cannot move at all')
                else:
                    end = [ m for m in possible_moves if m ][0]
                    if end:
                        log.debug(f'{start} can move to {end}')
                        ends[end].append(start)
                    else:
                        log.debug(f'{start} is blocked')

        return ends
        
    def move(self, mapp, moves):
    
        for start, end in moves:
            log.debug(f'moving {start} to {end}')
            mapp.map[end[1]][end[0]] = '#'
            mapp.map[start[1]][start[0]] = '.'
        return

    def A(self):
        
        mapp = self.get_input()

        for turn in range(10):
#           mapp.display()
            votes = self.vote(mapp, turn)
            moves = [ (v[0], k) for k, v in votes.items() if len(v) == 1 ]
            self.move(mapp, moves)

#       mapp.display()

        total = 0
        bounds = mapp.get_bounds()
        for y in range(bounds[0][1], bounds[1][1]):
            for x in range(bounds[0][0], bounds[1][0]):
                total += (1 if mapp.map[y][x] == '.' else 0)

        return total

    def B(self):

        mapp = self.get_input()
        turn = 0
        while True:
#       for i in range(25):
            votes = self.vote(mapp, turn)
            moves = [ (v[0], k) for k, v in votes.items() if len(v) == 1 ]
            if turn % 100 == 0: log.info(f'turn[{turn:04}]: moves: {len(moves)}')
            turn += 1
            if len(moves) == 0: break
            self.move(mapp, moves)

#       mapp.display()
        return turn

if __name__ == "__main__":
    AOC().run()
