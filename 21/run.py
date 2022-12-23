#!/usr/bin/env python3
import sys
sys.path.append('..')

import re
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=21)
        self.pattern = '(.*) (.) (.*)'

    def get_input(self):
        data = {}
        for l in super().get_input():
            k, v = l.split(': ')
            data[k] = v
        return data
 
    def eval(self, data, label):

        expr = data[label]
        
        m = re.match(self.pattern, expr)
        if m:
            x = self.eval(data, m.group(1))
            op = m.group(2)
            y = self.eval(data, m.group(3))
            if op == '+':
                total = x + y
            elif op == '-':
                total = x - y
            elif op == '*':
                total = x * y
            elif op == '/':
                total = x // y
            else:
                raise Exception(f'unknown operator: {op}')

        else:
            total = int(expr)

#       log.debug(f'{label} yells: {total}')
        return total

    def A(self):
        
        data = self.get_input()
        return self.eval(data, 'root')

    def B(self):

        data = self.get_input()
        data['humn'] = "0"
        humn = 0
        powinc = 9
        incr = 10 ** powinc
        log.info(f'starting search from {humn} with incr={incr}')
        while True:
            m = re.match(self.pattern, data['root'])
            assert m, 'failed to parse: {data["root"]}'
            x = self.eval(data, m.group(1))
            y = self.eval(data, m.group(3))
            diff = x - y
            if diff < 0:
                powinc -= 1
                oldhumn = humn
                humn -= incr
                incr = 10 ** powinc
                log.info(f'when humn={oldhumn}, diff={diff}, restarting search from {humn} with incr={incr}')
                data['humn'] = f'{humn}'
                continue
            else:
#           log.debug(f'{m.group(1)} yells {x}; {m.group(3)} yells {y} - a difference of {diff}')
                if x == y: break
                humn += incr
                data['humn'] = f'{humn}'
#           if humn > 305: break
    
        return humn

if __name__ == "__main__":
    AOC().run()
