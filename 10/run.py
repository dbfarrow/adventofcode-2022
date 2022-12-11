#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=10)

    def A(self):

        data = self.get_input()

        clock = 1
        x = 1
        v = None
        ready = True
        strength = 0

        while(True and clock <= 2000):
            
            # if we're ready for a new instruction, read it and reset
            # the v register and instruction clock counter (icc)
            if ready:
                l = data.pop(0) if len(data) > 0 else None
                if not l: break
                icc = 1
                v = 0

            # calculate completion state of the instruction
            if 'noop' in l:
                ready = True
                v = 0
            elif 'addx' in l:
                v = int(l.split(' ')[-1])
                ready = (icc == 2)
            else:
                raise Exception('huh?')
            
            # compute the value of strength if we're aligned on a proper clock boundary
            if ((clock - 20) % 40) == 0:
#               log.info(f'clock: {clock}, x: {x}, product: {clock*x}')
                strength += (clock * x)

#           log.info(f'during clock: {clock}: instr: {l:10}; x: {x}, v: {v}; ready: {ready}; icc: {icc}')
            # if the instruction has completed, do any instruction completion actions
            if ready:
                if 'addx' in l:
                    x += v
#           log.info(f'after  clock: {clock}: instr: {l:10}; x: {x}, v: {v}; ready: {ready}; icc: {icc}')

            # increment the clock
            clock += 1
            icc += 1
            
        return strength

    def B(self):

        data = self.get_input()

        clock = 1
        x = 1
        v = None
        crt = 0
        ready = True
        display = ''

        while(True):
            
            # if we're ready for a new instruction, read it and reset
            # the v register and instruction clock counter (icc)
            if ready:
                l = data.pop(0) if len(data) > 0 else None
                if not l: break
                icc = 1
                v = 0

            # calculate completion state of the instruction
            if 'noop' in l:
                ready = True
                v = 0
            elif 'addx' in l:
                v = int(l.split(' ')[-1])
                ready = (icc == 2)
            else:
                raise Exception('huh?')
            
            # if the sprite overlaps the current crt pos, oupput a '#' otherwise, output a '.'
            display += '#' if abs(crt - x) <= 1 else ' '
            crt += 1
            if crt % 40 == 0:
                log.info(display)
                display = ''
                crt = 0
 
#           log.info(f'during clock: {clock}: instr: {l:10}; x: {x}, v: {v}; ready: {ready}; icc: {icc}')
            # if the instruction has completed, do any instruction completion actions
            if ready:
                if 'addx' in l:
                    x += v
#           log.info(f'after  clock: {clock}: instr: {l:10}; x: {x}, v: {v}; ready: {ready}; icc: {icc}')

            # increment the clock
            clock += 1
            icc += 1
            
        # recording the actual answer here because i could hardly read it on my screen
        return 'REHPRLUB'

if __name__ == "__main__":
    AOC().run()
