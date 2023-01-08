#!/usr/bin/env python3
import sys
sys.path.append('..')

import json
from shared.aoc import __AOC
from shared import log

CHAMBER_WIDTH = 7
rocks = [
    [ 0b0011110 ],                                      #[ '####' ],
    [ 0b0001000, 0b0011100, 0b0001000 ],                #[ '.#.', '###', '.#.' ],
    [ 0b0000100, 0b0000100, 0b0011100 ],                #[ '..#', '..#', '###' ],
    [ 0b0010000, 0b0010000, 0b0010000, 0b0010000 ],     #[ '#', '#', '#', '#' ],
    [ 0b0011000, 0b0011000]                             # [ '##', '##' ],
]

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=17)

        self.chamber = list()
        self.heights = None

    def int_to_dstr(self, i):
        
        mask = 1<< 6
        dstr = ''
        while mask:
            dstr += '#' if mask & i else '.'
            mask >>= 1
        return f'|{dstr}|'

    def move(self, rock, height, move):

        # move the rock
        if move == '<' and not any([ s & 0b1000000 for s in rock ]):
            newrock = [ s << 1 for s in rock ]
        elif move == '>' and not any([ s & 1 for s in rock ]):
            newrock = [ s >> 1 for s in rock ]
        else:
            # the rock is blocked by a wall
            return rock

        # make sure the move doesn't collide with what's already in the chamber
        if any([ s & self.chamber[height - ix] for ix, s in enumerate(newrock) ]): return rock

        return newrock
 
    def display_rock(self, shape):
        for s in shape:
            log.trace(self.int_to_dstr(s))
        log.trace('')

    def display_chamber(self, floor = 0):

        for i in range(len(self.chamber) - 1, floor - 1, -1):
            log.trace(f'{i:02} {self.int_to_dstr(self.chamber[i])}')
        log.trace('   +-------+')
        log.trace('') 

    def drop_rock(self, shape):

        # for each rock we start by making sure there
        # are three empty rows above the top rock so that we can move
        # the rock left and right unimpeded before we hit the top of
        # the stack. 
        pad = 3 + len(shape)
#       log.debug(f' padding chamber by {pad}')
        for i in range(pad):
            self.chamber.append(0)
#       self.display_chamber()
 
        return len(self.chamber)

    def can_fall(self, rock, height):
        if height - len(rock) < 0: return False
        return not any([ s & self.chamber[height - 1 - ix] for ix, s in enumerate(rock) ])
        
    def save_rock(self, rock, height):
        rock_bottom = height - len(rock) + 1
#       log.debug(f'  saving rock at {height}, rock bottom at {rock_bottom}')
        for ix, r in enumerate(reversed(rock)):
            self.chamber[rock_bottom + ix] |= r
    
    def solve(self, inp, max_rocks):

        heights = []
        clicks = 0
        for rock_num in range(max_rocks):
            
            # the next shape appears. select the shape
            # and add three blank rows to the end of the
            # chamber
            rock = rocks[rock_num % len(rocks)]
            start_height = self.drop_rock(rock)
#           log.debug(f'Dropping rock #{rock_num:05} at height {start_height}')
            
            # then we alternate between moving and falling until
            # the rock can no longer fall
            for doot in range(start_height, 0, -1):

                height = doot - 1 
                # get the next move 
                move = inp[clicks % len(inp)]
                clicks += 1
#               log.debug(f'  processing move: {move}')

                # calculate the left/right move
                moved = self.move(rock, height, move)
#               self.display_rock(moved)                

                # check if we can fall. if not, add the rock to the
                # chamber at the current ix and break out
                log.debug(f'  checking if rock can fall from {height}')
                if self.can_fall(moved, height):
                    rock = moved
#                   log.debug('    it can; keep falling')
#                   self.display_rock(rock)
                else:
#                   log.debug('    it cannot; save the rock at this height')
#                   self.display_rock(moved)
                    break
                
            self.save_rock(moved, height)
            
            # gross hack... remove all the empty rows from the top of the chamber
            for i in range(len(self.chamber), 0, -1):
                if self.chamber[i - 1] != 0: break
            self.chamber = self.chamber[0:i]
                 
#           self.display_chamber()
#           if rock_num > 8: break
            heights.append(len(self.chamber))

        return len(self.chamber), heights

    def validate_repeats(self, deltas, repeats, window):

        test = set()
        doot = deltas[repeats:]
        ndoots = len(doot) // window
        doot = doot[0:ndoots*window]
        for i in range(ndoots):
            zzz = ''.join([ str(d) for d in doot[i*window:i*window+window] ])
            test.add(zzz)

        return len(test) == 1

    def A(self):

        answer, self.heights = self.solve(self.get_input()[0], 2022)
        return answer

    def B(self):

        inp = self.get_input()[0]

        for i in range(1, (len(inp) // 2022) * 2):

            max_rocks = 2022 * i
            log.info(f'checking for repeating pattern in {max_rocks} falling')

            answer, heights = self.solve(self.get_input()[0], max_rocks)
            deltas = [ heights[i+1] - heights[i] for i in range(len(heights) - 1) ]
            assert not any([ d for d in deltas if d >= 10 ]), 'that will not work'
            deltastr = ''.join([ str(d) for d in deltas ])

            repeats = -1
            for window in range(len(deltastr) // 3, 0, -1):
                for offset in range(len(deltastr) - window):
                    a = deltastr[offset:offset+window]
                    b = deltastr[offset+window:offset+window+window]
                    if b == a:
                        repeats = offset
                        break

                if repeats > 0: break

            if self.validate_repeats(deltas, repeats, window):
                log.info(f'  found repeating pattern')
                break
            else:
                log.info(f'  repeats={repeats}, window={window} failed validation check')

        assert repeats > 0, 'no repeating pattern found in stacking. cannot solve with this method'
        log.info(f'stacking pattern repeats at {offset} with a window size of {window}')

        # Now calculate the height of the stoopidly large stack
        max_rocks = 1000000000000

        num_deltas = max_rocks - repeats - 1
        num_repeats = (num_deltas - repeats) // window
        each_repeat = sum(deltas[repeats:repeats+window])
        remaining = max_rocks - repeats - (num_repeats * window)

        before = sum(deltas[0:repeats]) 
        after = sum(deltas[repeats:repeats+remaining]) 

        total = before + (num_repeats * each_repeat) + after
        return total

if __name__ == "__main__":
    AOC().run()
