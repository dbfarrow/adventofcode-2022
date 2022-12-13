#!/usr/bin/env python3
import sys
sys.path.append('..')

from functools import cmp_to_key
from lark import Lark, Transformer, v_args

from shared.aoc import __AOC
from shared import log

class TreeToList(Transformer):
    list = list
    number = v_args(inline=True)(int)

input_parser = Lark(r'''

    ?start: value

    ?value: list
         | NUMBER    -> number

    list : "[" [value ("," value)*] "]"

    %import common.NUMBER
    %import common.WS
    %ignore WS

''', parser='lalr', lexer='basic', transformer=TreeToList())

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=13)

    def compare_lists(self, a, b):
        
        a = [ i for i in a if i != None ]
        b = [ i for i in b if i != None ]
    
#       log.info(f'comparing: {a} <> {b}')
        for i in range(len(a)):
            va = a[i]
            try:
                vb = b[i]
            except:
                # out of items
                raise Exception('b is out of items at index {i}')
    
            tva = type(va)
            tvb = type(vb)
    
            if (tva == int) and (tvb == int):
                if va < vb:
#                   log.info(f'a < b; good signal at i={i} ( {va} < {vb} )')
                    return True
                elif va > vb:
                    raise Exception(f'a > b; bad signal at i={i} ( {va} > {vb} )')
    
            if (tva == list) and (tvb == list) and self.compare_lists(va, vb):
#               log.info('recursion; good signal')
                return True
            if (tva == list) and (tvb != list) and self.compare_lists(va, [ vb ]):
#               log.info('[ vb ] + recursion; good signal')
                return True
            if (tva != list) and (tvb == list) and self.compare_lists([ va ], vb):
#               log.info('[ va ] + recursion; good signal')
                return True
    
        if len(a) < len(b): 
#           log.info('a is out of items')
            return True
    
#       log.info('no clear good signal; keep looking')
        return False
    
    def compare_signals(self, a, b):
    
        a = input_parser.parse(a)
        b = input_parser.parse(b)
        try:
            good = self.compare_lists(a, b)
        except Exception as e:
#           log.info(f'definitive bad signal order detected: {e}')
            good = False
    
#       log.info(f'{a} <> {b} == {good}')
#       log.info('')
        return good
    
    def comparator(self, a, b):
        return -1 if self.compare_signals(a, b) else 1

    def A(self):

        lines = self.get_input()
        npairs = (len(lines) + 1) // 3
    
        comparisons = { i+1: self.compare_signals(lines[i*3], lines[i*3+1]) for i in range(npairs) }
        good_signals = [ i for i in comparisons if comparisons[i] ]
#       log.info(good_signals)
        return sum(good_signals)

    def B(self):

        signals = [ l for l in self.get_input() if len(l) > 0 ]
        decoder = [ "[[2]]", "[[6]]" ]
        signals.extend(decoder)

        signals = sorted(signals, key=cmp_to_key(self.comparator))    
        answer = 1
        for ix, s in enumerate(signals):
            if s in decoder: answer *= (ix + 1)
#           log.info(s)

        return answer

if __name__ == "__main__":
    AOC().run()
