#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

CHAMBER_WIDTH = 7
shapes = [
    [ 0b0011110 ],                                        #[ '####' ],
    [ 0b0001000, 0b0011100, 0b0001000 ],              #[ '.#.', '###', '.#.' ],
    [ 0b0000100, 0b0000100, 0b0011100 ],              #[ '..#', '..#', '###' ],
    [ 0b0010000, 0b0010000, 0b0010000, 0b0010000 ], #[ '#', '#', '#', '#' ],
    [ 0b0011000, 0b0011000]                             # [ '##', '##' ],
]

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=17)

        self.chamber = list()
        self.floor = 0

    def shape_appears(self, n):
        
        # push three emtpy lines on top of the chamber and add the shape
        # and make the shape appear
        self.chamber.extend([ 0, 0, 0])
        self.chamber.extend(reversed(shapes[n]))

    def int_to_dstr(self, i):
        
        mask = 1<< 6
        dstr = ''
        while mask:
            dstr += '#' if mask & i else '.'
            mask >>= 1
        return f'|{dstr}|'

    def move_right(self, shape, origin):

        log.debug(f'moving shape {shape} right one space from {origin}')

        # make sure the shape isn't already up against the right edge
#       for s in shapes[shape]::q

        return
 
    def display_chamber(self):

        for i in range(len(self.chamber) - 1, self.floor, -1):
            log.info(self.int_to_dstr(self.chamber[i]))
        log.info('---------')
        log.info('') 

    def A(self):

        inp = self.get_input()[0]
        log.info(inp)

        shape_count = 0
        clicks = 0
        while shape_count < 1:

            # the next shape appears
            shape = shape_count % len(shapes)
            self.shape_appears(shape)
            origin = (2, len(self.chamber) - 1)
            self.display_chamber()

            while True:
                move = inp[clicks % len(inp)]
                log.debug(f'processing move: {move}')
                if move == '>':
                    self.move_right(shape, origin)
                clicks += 1
                break

            shape_count += 1
            
        return None

    def B(self):
        return None

if __name__ == "__main__":
    AOC().run()
