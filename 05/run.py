#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
import re

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=5)

    def get_input(self):
        lines = super().get_input()
        
        # parse the initial crate state
        crates = defaultdict(list)
        for ix, l in enumerate(lines):
            if l[1] == '1': break       # the end of the section is marked by the line ' 1 2 3 ...'

            for i in range((len(l)+1)//4):
                crate = l[i*4+1]
                if crate != ' ':
                    crates[i+1].append(crate)

        # parse the moves
        moves = []
        expr = 'move ([0-9]+) from ([0-9]+) to ([0-9]+)'
        p = re.compile(expr)
        for i in range(ix+2, len(lines)):
            m = p.match(lines[i])
            assert m, f'failed to parse "{lines[i]}" for a move'
            moves.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))

        # print the crates and moves for debugging purposes
        if self.cmdline.verbose:
            self.print_stacks(crates)
            for m in moves:
                log.debug(m)

        # and return the data
        return (crates, moves)

    def print_stacks(self, crates):
        for k in sorted(crates.keys()):
            log.info(f'{k}: {crates[k]}')
        log.info(' ')
 
    def make_move(self, move, crates, reverse):
        (n, src, dest) = move
        to_move = crates[src][0:n]
        if reverse: to_move.reverse()
        crates[dest] = to_move + crates[dest]
        crates[src] = crates[src][n:]
        if crates[src] == None: crates[src] = []

    def A(self):
        (crates, moves) = self.get_input()
        for m in moves:
            self.make_move(m, crates, reverse=True)

        # should return SVFDLGLWV
        return ''.join([ crates[i][0] for i in sorted(crates.keys()) ])

    def B(self):
        (crates, moves) = self.get_input()
        for m in moves:
            self.make_move(m, crates, reverse=False)

        # should return DCVTCVPCL
        return ''.join([ crates[i][0] for i in sorted(crates.keys()) ])

if __name__ == "__main__":
    AOC().run()
