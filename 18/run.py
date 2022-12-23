#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from functools import reduce
from itertools import permutations
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=18)

    def get_input(self):
        cubes = list()
        for l in super().get_input():
            (x, y, z) = map(int, l.split(','))
            # shift the inputs by (2, 2, 2) so we know there is room around the 
            # shape to flood the area when calculating part 2
            cubes.append((x + 2, y + 2, z + 2)) 

        return cubes

    def calc_touching_edges(self, cubes):

        num_edges = 0
        for perm in permutations([ 0, 1, 2]):
            (x, y, z) = perm
            stacks = defaultdict(list)
            for c in cubes:
                stacks[(c[x], c[y])].append(c[z])                

            for stack in stacks.values():
                stack.sort()
                for c in range(len(stack) - 1):
                    if stack[c + 1] - stack[c] == 1:
                        num_edges += 1

        return num_edges

    def find_trapped(self, cubes):

        trapped = []
        
        mins = [ min([ c[i] for c in cubes ]) for i in range(3) ]
        maxs = [ max([ c[i] for c in cubes ]) for i in range(3) ]
        log.debug(mins)
        log.debug(maxs)

        for x in range(mins[0], maxs[0] + 1):
            for y in range(mins[1], maxs[1] + 1):
                for z in range(mins[2], maxs[2] + 1):
                    if (x - 1, y, z) not in cubes: continue
                    if (x + 1, y, z) not in cubes: continue
                    if (x, y + 1, z) not in cubes: continue
                    if (x, y - 1, z) not in cubes: continue
                    if (x, y, z + 1) not in cubes: continue
                    if (x, y, z - 1) not in cubes: continue
                    if (x, y, z) in cubes: continue
                    log.debug(f'cube at {x}, {y}, {z} is trapped air')
                    trapped.append((x, y, z))

        log.info(f'{len(trapped)} locations out of {len(cubes)} are completely surrounded')
        return trapped

    def neighbors(self, p, maxs):
        (x, y, z) = p
        ns = [
            (x - 1, y, z),
            (x + 1, y, z),
            (x, y + 1, z), 
            (x, y - 1, z), 
            (x, y, z + 1), 
            (x, y, z - 1), 
        ]
        ns = [ n for n in ns if n[0] <= maxs[0] and n[1] <= maxs[1] and n[2] <= maxs[2] ]
        ns = [ n for n in ns if n[0] >= 0 and n[1] >= 0 and n[2] >= 0 ]
        log.debug(f'neighbors of {p}: {ns}')
        return ns
        
    def A(self):

        cubes = self.get_input()
        sa = len(cubes) * 6 - self.calc_touching_edges(cubes)
        return sa

    def B(self):

        cubes = self.get_input()
        maxs = [ max([ c[i]+2 for c in cubes ]) for i in range(3) ]

        visited = []
        to_visit = [ (0, 0, 0) ]
        sa = 0
 
        space_size = reduce((lambda x, y: x * y), [ x + 2 for x in maxs ])
        log.debug(maxs)
        log.debug(f'max space size is {space_size} points')

        for p in to_visit:
            visited.append(p)
            for n in self.neighbors(p, maxs):

                if n in visited: continue
                if n in to_visit: continue

                if n in cubes:
                    log.debug(f'{n} in cubes')
                    sa += 1
                else:
                    to_visit.append(n)

        log.info(f'the method of subracting trapped air edges from the total in part 1 yields: {self.b()}')

        return sa

    # No idea why this doesn't work
    def b(self):

        cubes = self.get_input()
        trapped = self.find_trapped(cubes) 
        trapped_edges = self.calc_touching_edges(trapped)
        log.debug(f'trapped: count = {len(trapped)} of {len(cubes)}')
        log.debug(f'trapped_edges: {trapped_edges}')
        for t in trapped:
            log.debug(t)
        sa = (len(cubes) * 6 - self.calc_touching_edges(cubes)) - (len(trapped) * 6)
        return sa

if __name__ == "__main__":
    AOC().run()
