#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=22)

        self.movement = {
            'N': { 'move': (0, -1), 'L': 'W', 'R': 'E', 'score': 3 },
            'S': { 'move': (0,  1), 'L': 'E', 'R': 'W', 'score': 1 },
            'E': { 'move': (1,  0), 'L': 'N', 'R': 'S', 'score': 0 },
            'W': { 'move': (-1, 0), 'L': 'S', 'R': 'N', 'score': 2 },
        }
        self.paths = defaultdict(int)

    def get_input(self):

        lines = super().get_input()
        mapp = []
        
        for ix, l in enumerate(lines):
            if len(l) > 0:
                mapp.append(l)
            else:
                ix += 1 # to skip the blank line
                break

        map_width = max(set([ len(l) for l in mapp ]))
        mapp = [ (l + (' '*map_width))[0:map_width] for l in mapp ]

        # parse the directions
        dirs = []
        for i in range(ix, len(lines)):
            l = lines[i]
            if l[0] == ';': continue

            tmpstr = ''
            for c in l:
                if c.isdigit():
                    tmpstr += c
                else:
                    dirs.append((int(tmpstr), c))
                    tmpstr = ''
 
        return (mapp, dirs)

    def find_start(self, mapp):

        for y, r in enumerate(mapp):
            for x, c in enumerate(r):
                if c == '.': return (x, y)
                    
        raise Exception('cannot find start of map')

    def move(self, mapp, start, dirs):

        log.debug(f'moving {dirs[0]} spaces {start[1]} from {start[0]} then turning {dirs[1]}')

        movement = self.movement[start[1]]
        end = start[0]
        for i in range(dirs[0]):

            try:
                x = end[0] + movement['move'][0]
                y = end[1] + movement['move'][1]
                if start[1] in [ 'E', 'W' ]:
                    if (x >= len(mapp[y])) or ((mapp[y][x] == ' ') and start[1] == 'E'):
                        # wrap around the right edge
                        x -= 1
                        while (x >= 0 and (mapp[y][x] != ' ')): 
                            x -= 1
                        x += 1
                        log.debug(f'wrapping x around right edge to {x}')
                        self.paths['right'] += 1

                    elif (x < 0) or ((mapp[y][x] == ' ') and start[1] == 'W'):
                        # wrap around the left edge
                        x += 1
                        while (x < len(mapp[y]) and (mapp[y][x] != ' ')):
                            x += 1
                        x -= 1
                        log.debug(f'wrapping x around left edge to {x}')
                        self.paths['left'] += 1
                
                if start[1] in [ 'N', 'S' ]:
                    if (y >= len(mapp)) or ((mapp[y][x] == ' ') and start[1] == 'S'):
                        y -= 1
                        while (y >= 0) and (mapp[y][x] != ' '):
                            y -= 1
                        y += 1
                        log.debug(f'wrapping y around bottom edge to {y}')
                        self.paths['bottom'] += 1

                    elif (y < 0) or ((mapp[y][x] == ' ') and start[1] == 'N'):
                        y += 1
                        while (y < len(mapp)) and (mapp[y][x] != ' '):
                            y += 1
                        y -= 1
                        log.debug(f'wrapping y around top edge to {y}')
                        self.paths['top'] += 1
    
                log.debug((x, y))
                if mapp[y][x] == '#':
                    log.debug(f'cannot move to {x},{y} because of a wall')
                    break
                else:
                    end = (x, y)
            except Exception as e:
                log.failure(f'exception {e} at ({x}, {y})')
                log.failure(f'start: {start}')
                log.failure(f'move : {dirs}')
                log.failure(f'mapp length: {len(mapp)}')
                log.failure(f'mapp width : {len(mapp[0])}')
                log.failure(f'mapp width on row {y}: {len(mapp[y])}')
                raise e

        return (end, movement[dirs[1]])

    def display(self, mapp):
        for r in mapp:
            log.info(r)
        log.info('')

    def A(self):

        mapp, dirs = self.get_input()
        pos = (self.find_start(mapp), 'E')
        log.info(pos)
        
        for dd in dirs:
            pos = self.move(mapp, pos, dd)
            log.debug(pos)
            log.debug('')

        log.info(f'ended at: {pos}')
        coord = pos[0]
        ddir = pos[1]
        passwd = (1000 * (coord[1] + 1)) + (4 * (coord[0] + 1)) + self.movement[ddir]['score']

        for  p in self.paths:
            log.info(f'{p}: {self.paths[p]}')

        return passwd

    def B(self):
        return None

if __name__ == "__main__":
    AOC().run()
