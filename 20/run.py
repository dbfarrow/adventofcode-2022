#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=20)

    def get_input(self):
        return list(map(int, super().get_input()))

    def get_offset(self, ix, enc, dec):

        # get *all* instances of the value at enc[ix] between enc[0] and enc[ix]
        # to tell us *which* instance of the value we need to be looking for
        # in dec
        es = [ e for e in enc[0:ix + 1] if e == enc[ix] ]
        e = enc[ix]
        if len(es) > 1:
            log.debug(f'looking for instance number {len(es)} of {enc[ix]}')
            offset = 0
            for i in range(len(es)):
                log.info(f'   starting search for {e} at {offset}') 
                offset = dec.index(e, offset) 
                log.info(f'   found an instance at {offset}') 
        else:
            offset = dec.index(enc[ix])

        return offset

    def A(self):

        enc = self.get_input()
        dec = self.get_input()
        wrap = len(enc)

        log.debug(dec)

        for ix, e in enumerate(enc):

            # locate e in the decryption buffer
            x = self.get_offset(ix,enc, dec)
#           log.debug(f'value {e} is found at index {x} of enc')
            if e == 0: 
#               log.debug(dec)
                continue

            dec.pop(x)
            new_pos = (x + e) % (wrap - 1)
            if new_pos == 0:
                new_pos = wrap if e < 0 else 0

#           log.debug(f'{ix}: {e} starts at {x} and moves to {new_pos}')
            dec.insert(new_pos, e)
#           log.debug(dec)
        
        zpos = dec.index(0)
        for i in range(1, 4):
            x = ((i * 1000) + zpos) % wrap
            log.debug(f'dec[{x}]: {dec[x]}')

        return sum([ dec[((i * 1000) + zpos) % wrap] for i in range(1, 4) ])

    def B(self):
        return None

if __name__ == "__main__":
    AOC().run()
