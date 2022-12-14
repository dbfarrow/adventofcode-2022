#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from shared.aoc import __AOC
from shared import log

class Cave:

    def __init__(self, data, entry = 500):
        
        self.area = defaultdict(dict)
        self.full = False
        self.grains = 0
        self.bail_after = 1000 * 1000

        self.grain_entry_x = entry
        self.min_x = self.grain_entry_x
        self.max_x = self.grain_entry_x
        self.min_y = 0
        self.max_y = 0

        for l in data:
            segments = [ s.split(',') for s in l.split(' -> ') ]
            for i in range(len(segments) - 1):
                ax = int(segments[i][0])
                ay = int(segments[i][1])
                bx = int(segments[i+1][0])
                by = int(segments[i+1][1])
                xinc = 1 if ax <= bx else -1
                yinc = 1 if ay <= by else -1

                log.debug(f'parsing segment from {ax},{ay} to {bx},{by}')
                for x in range(ax, bx + xinc, xinc):
                    for y in range(ay, by + yinc, yinc):
                        self.area[y][x] = '#'

                self.min_x = min([ax, bx, self.min_x]) - 1
                self.min_y = min([ay, by, self.min_y])
                self.max_x = max([ax, bx, self.max_x]) + 1
                self.max_y = max([ay, by, self.max_y])
        
        log.debug(f'visible cave bounds: ({self.min_x},{self.min_y}) -> ({self.max_x},{self.max_y})')

    def add_floor(self, depth = 2):
   
        floor_y = self.max_y + depth
 
        # the floor will extend n spaces in each direction left and right of the sand
        # entry point where n is the y location of the floor. we need to expand
        # the bounds of the area to cover this
        self.min_x = min(self.min_x, self.grain_entry_x - floor_y)
        self.max_x = max(self.max_x, self.grain_entry_x + floor_y)

        self.area[floor_y] = { x: '#' for x in range(self.min_x, self.max_x + 1) }
        self.max_y = floor_y

    def add_grain(self):
        
        x = self.grain_entry_x
        y = 0

        while True:

            if self.area[y].get(x) == 'o':
                log.info(f'reached top of cave at {self.grains} grains')
                self.full = True
                return
            elif y >= self.max_y:
                # if we've fallen out the botton, the area is full
                log.info(f'grains fall off at {self.grains} grains')
                self.full = True
                return
            elif not self.area[y+1].get(x):
                y += 1
            elif not self.area[y+1].get(x-1):
                y += 1
                x -= 1
            elif not self.area[y+1].get(x+1):
                y += 1
                x += 1
            else:
                # we've reached a terminal point
                break

        self.area[y][x] = 'o'
        self.grains += 1
        self.full = (self.grains >= self.bail_after)
            
    def draw(self):
        
        # draw the header
        header = [ f'{i: 4}' for i in range(self.min_x, self.max_x + 1) ]
        for ix in range(4):
            t = ''
            for h in header:
                t += (h[ix])
            log.debug(f'     {t}')

        # draw the map of the area
        for y in range(self.min_y, self.max_y + 1):
            if y in self.area:
                row = ''.join([ self.area[y].get(x, ' ') for x in range(self.min_x, self.max_x + 1) ])
            else:
                row = ' ' * (self.max_x - self.min_x)
            log.debug(f'{y:04} {row}')


class AOC(__AOC):

    def __init__(self):
        super().__init__(day=14)

    def A(self):

        cave = Cave(self.get_input())
        cave.draw()
        while not cave.full:
            cave.add_grain()

        cave.draw()
        return cave.grains

    def B(self):

        cave = Cave(self.get_input())
        cave.add_floor()

        while not cave.full:
            cave.add_grain()
        cave.draw()

        return cave.grains

if __name__ == "__main__":
    AOC().run()
