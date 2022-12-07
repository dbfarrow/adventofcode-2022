#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from enum import Enum
import json
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=7)
 
    def cd(self, stack, d):
        if d == '..':
            if len(stack) > 1:      # only pop the stack if we aren't at the top
                stack = stack[0:-1]
#               log.info(f'popping stack: {stack}')
                return stack
        else:
#           log.info(f'cd:stack: {stack}; d = {d}')
            path = ''
            if len(stack) == 0:
                path = '/'
            elif len(stack) == 1:
                path = f'/{d}'
            else:
                path = f'{stack[-1]}/{d}'
#           log.info(f'new path = {path}')
            stack.append(path) 
#       log.info(stack)
        return stack

    def add(self, stack, dirs, size):
        for s in stack:
            dirs[s] += size
             
    def calc_dir_sizes(self, lines):
        dirs = defaultdict(int)
        stack = []
        for l in self.get_input():
            parts = l.split(' ')
            if parts[0] == '$':      # this is a command
                if parts[1] == 'cd':
                    stack = self.cd(stack, parts[2])
            else:                   # this is the output of an ls command
                if parts[0] != 'dir':
                    self.add(stack, dirs, int(parts[0]))
        return dirs

    def A(self):
        dirs = self.calc_dir_sizes(self.get_input())
        return sum([ v for v in dirs.values() if v <= 100000])

    def B(self):
        dirs = self.calc_dir_sizes(self.get_input())
        needed = 30000000 - (70000000 - dirs['/'])
        return min([ v for v in dirs.values() if v > needed ])

if __name__ == "__main__":
    AOC().run()
