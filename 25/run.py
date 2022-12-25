#!/usr/bin/env python3
import sys
sys.path.append('..')

import math
from shared.aoc import __AOC
from shared import log

symbols = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=25)

    def snafu_to_dec(self, s):

        log.debug(f'{s} is composed of')

        d = 0
        for ix, c in enumerate(s):
            delta = symbols[c] * (5 ** (len(s) - ix - 1))
            d += delta 
            log.debug(delta)
        return d

    def dec_to_snafu(self, d):
    
        msd = math.floor(math.log(d, 5)) + 1
        s = ''

        for msd in range(msd, -1, -1):
            place = 5 ** msd
            for k, v in symbols.items():
                rM = (v * place) + (place // 2)
                rm = rM - place
                if rm <  d <= rM:
                    s += k
                    delta = v * place
                    log.debug(f'k: {k}, v: {v}, place: {place}, {rm} <= {d} <= {rM}, delta: {delta}, new d: {d - delta}')
                    d -= delta
                    break
                else:
                    log.debug(f'k: {k}, v: {v}, place: {place}, {rm} !< {d} !< {rM}')

            log.debug(f'msd: {msd}, place: {place}, s: {s}, d: {d}')
            log.debug('')

        return s.lstrip('0')

        while d != 0:
            msd = math.floor(math.log(abs(d), 5)) + 1
            log.debug(f'msd of {d} is {msd}')
            log.debug(f'5 ** {msd} = {5 ** msd}') 
            r = math.floor(d / (5 ** msd)) + 1
            log.debug(f'r = {r}')
            s += slobmys[r]

            d -= r * (5 ** msd)
            
            log.debug(f's: {s}; d: {d}')

            if len(s) >= 2: 
                log.debug('bork')
                break

        return 0


    def A(self):

        dec = sum([ self.snafu_to_dec(s) for s in self.get_input() ])
        log.info(f'decimal = {dec}')
        return self.dec_to_snafu(dec)

    def B(self):
        return None

if __name__ == "__main__":
    AOC().run()
