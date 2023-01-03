#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=24)

    def get_input(self):

        data = super().get_input()
        return [ [ [ col ] for col in row ] for row in data ]

    def print_map(self, mapp):
        
        for row in mapp:
            rowstr = ''
            for col in row:
                if len(col) == 1:
                    rowstr += col[0]
                else:
                    rowstr += str(len(col))
            log.trace(rowstr)
        log.trace('')

    def find_end(self, mapp):
        return len(mapp[0]) - 2, len(mapp) - 1 

    def move_blizzards(self, mapp):

        nrows = len(mapp)
        ncols = len(mapp[0])
        newmapp = [[ [] for x in range(ncols) ] for y in range(nrows) ]

        for r in range(nrows):
            for c in range(ncols):
                vs = mapp[r][c]
                mapp[r][c] = []
                for v in vs:
                    if v == '#':
                        newr = r
                        newc = c
                    elif v == '.':
                        continue
                    elif v == '>':
                        newc = c + 1 if c <  (ncols - 2) else 1
                        newr = r
                    elif v == '<':
                        newc = c - 1 if c > 1 else (ncols - 2)
                        newr = r
                    elif v == 'v':
                        newc = c
                        newr = r + 1 if r < (nrows - 2) else 1
                    elif v == '^':
                        newc = c
                        newr = r - 1 if r > 1 else (nrows - 2)
                    else:
                        log.info(v)

                    newmapp[newr][newc].append(v)

        for r in range(nrows):
            for c in range(ncols):
                if len(newmapp[r][c]) == 0:
                    newmapp[r][c].append('.')
        return newmapp

    def find_moves(self, mapp, moves):

        newmoves = set()
        adj = [ (1,0), (0,1), (-1,0), (0,-1) ]
        for m in moves:
            has_move = False
            for a in adj:
                col = m[0] + a[0]
                row = m[1] + a[1] 
                if row < 0 or col < 0: continue
                if row >= len(mapp) or col >= len(mapp[0]): continue
                v = mapp[row][col]
 
                if len(v) == 1: v = v[0]
                if v == '.':
                    newmoves.add((col, row))
                    has_move = True


            # standing still is also a valid move. let's leave it
            # in as a possibility
            v = mapp[m[1]][m[0]] 
            if (len(v) == 1) and (v[0] == '.'):
                newmoves.add(m)
                     
        return list(newmoves)

    def travel(self, mapp, start, end):

        log.info(f'searching for path through storm from {start} to {end}')
        
        moves = [ start ]
        done = False
        time = 1
        while True:
            log.debug(f'Time: {time}')
            mapp = self.move_blizzards(mapp)
            moves = self.find_moves(mapp, moves)
            log.debug(f'  possible moves: {moves}')
            if end in moves: break
            time += 1

            if self.cmdline.testing and time > 100: break

        return time, mapp

    def A(self):

        mapp = self.get_input()
        start = (1, 0)
        end = self.find_end(mapp)
        time, mapp = self.travel(mapp, start, end)
        return time

    def B(self):

        mapp = self.get_input()
        start = (1, 0)
        end = self.find_end(mapp)
 
        total = 0
        time, mapp = self.travel(mapp, start, end)
        total += time
 
        self.print_map(mapp)
        time, mapp = self.travel(mapp, end, start)
        total += time

        time, mapp = self.travel(mapp, start, end)
        total += time

        return total

if __name__ == "__main__":
    AOC().run()
