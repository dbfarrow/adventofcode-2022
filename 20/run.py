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

    def get_offset(self, eix, dec):
        loc = [ ix for ix, de in enumerate(dec) if de[1] == eix ]
        assert len(loc) == 1, 'wt?'
        return loc[0]

    def decode(self, dec, wrap):

        dec = [ d[0] for d in dec ]
        zpos = dec.index(0)
        for i in range(1, 4):
            x = ((i * 1000) + zpos) % wrap
            log.debug(f'dec[{x}]: {dec[x]}')

        return sum([ dec[((i * 1000) + zpos) % wrap] for i in range(1, 4) ])

    def mix(self, enc, dec, wrap):

        for ix, e in enumerate(enc):

            # locate e in the decryption buffer
            x = self.get_offset(ix, dec)
            log.debug(f'value {e} is found at index {x} of enc')
            if e == 0: 
                log.debug([ d[0] for d in dec ])
                continue

            dec.pop(x)
            new_pos = (x + e) % (wrap - 1)
            if new_pos == 0:
                new_pos = wrap if e < 0 else 0

            log.debug(f'{e} starts at {x} and moves to {new_pos}')
            dec.insert(new_pos, (e, ix))
            log.debug([ d[0] for d in dec ])
        
        return dec

    def A(self):
        enc = self.get_input()
        dec = [ (e, ix) for ix, e in enumerate(enc) ]
        wrap = len(dec)
        mixed = self.mix(enc, dec, wrap)
        return self.decode(mixed, wrap)        

    def B(self):
        enc = [ 811589153 * e for e in self.get_input() ]
        dec = [ (e, ix) for ix, e in enumerate(enc) ]
        wrap = len(enc)

        log.debug([ d[0] for d in dec ])
        for i in range(10):
            dec = self.mix(enc, dec, wrap)
            log.debug([ d[0] for d in dec ])
 
        return self.decode(dec, wrap)

if __name__ == "__main__":
    AOC().run()
