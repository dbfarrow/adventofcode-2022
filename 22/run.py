#!/usr/bin/env python3 
import sys
sys.path.append('..')

from item import Item
from sides import parse_sides
from junglemap import FlatMap, CubeMap
from collections import defaultdict
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=22)

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
                    dirs.extend([int(tmpstr), c])
                    tmpstr = ''

            # get the last move. this bit me right in the butt
            dirs.append(int(tmpstr))
 
        return (mapp, dirs)

    def solve(self, mapp, dirs, maptype, pos = None):

        if not pos:
            pos = ((8, 0), '>') if self.cmdline.testing else ((50, 0), '>')

        actual = []
        while len(dirs) > 0:
            num_steps = dirs.pop(0)
            turn_dir = dirs.pop(0) if len(dirs) > 0 else None
            log.debug(f'-------')
            log.debug(f'moving {num_steps} steps heading {pos[1]} from {pos[0]} then turning {turn_dir}')
            path = maptype(mapp, pos)
            for i in range(num_steps):
                moved = path.next()
                if moved:
                    log.debug(f'  new position: {path.current}')
                else:
                    log.debug(f'  path blocked at {path.current}')
                    break
            if moved: i += 1
            actual.extend([i, turn_dir])
            old_heading = pos[1]
            new_heading = path.calc_turn(path.current, turn_dir)
            log.debug(f'reached destination for this leg at {path.current}. turning {turn_dir} from old heading {old_heading} to {new_heading}')
            pos = ((path.current.x, path.current.y), new_heading)
            log.debug(f'')

        pos = path.unrotate(pos)
        return pos, actual

    def calc_score(self, pos):
        scores = [ '>', 'v', '<', '^' ]
        col, row = pos[0]
        heading = pos[1]
        log.debug(f'calc_score: row: {row}, col: {col}, heading: {heading}')
        return ((row + 1) * 1000) + ((col + 1) * 4) + scores.index(heading) 
 
    def parse_cmdline_extra(self, parser):
        parser.add_argument('--test_cubes', action='store_true', default=False)
        parser.add_argument('--backtrack', action='store_true', default=False)

    def A(self):
        mapp, dirs = self.get_input()
        end, actual =  self.solve(mapp, dirs, FlatMap)
        return self.calc_score(end)

    def B(self):

        mapp, dirs = self.get_input()

        if not self.cmdline.test_cubes:
            end, actual =  self.solve(mapp, dirs, CubeMap)
            pw = self.calc_score(end)
            log.info(f'path ended at {end} with pw={pw}')

            if self.cmdline.backtrack:
                # FOR DEBUGGING
                # retrace our steps to see if we end up at the start like we should
                # compute the return path from the actual path taken
                path_back = []
                for s in actual:
                    if s == None: continue
                    elif s == 'R': path_back.insert(0, 'L')
                    elif s == 'L': path_back.insert(0, 'R')
                    else: path_back.insert(0, s)
        
                headings = [ '>', 'v', '<', '^' ]
                reverse_heading = headings[(headings.index(end[1]) + 2) % 4]
                end = (end[0], reverse_heading)
                log.info(f'retracing our steps from {end}') 
                end, actual = self.solve(mapp, path_back, CubeMap, end)
                log.info(f'    we are at: {end}') 

            return pw

if __name__ == "__main__":
    AOC().run()
