#!/usr/bin/env python3
import sys
sys.path.append('..')

import argparse
from collections import defaultdict
from item import Item
from sides import parse_sides
from shared import log

CLOCKWISE = 0
COUNTERCLOCKWISE = 1

class BaseMap:

    def __init__(self, mapp, pos):

        self.mapp = mapp
        self.x, self.y = pos[0]
        self.heading = pos[1]
        self.preinit()

        # create the list of items
        self.items = self.get_items(mapp)
        self.link_items()

    def link_items(self):

        # then link them together
        for i in range(len(self.items) - 1):
            self.items[i].next = self.items[i + 1]
            self.items[i + 1].prev = self.items[i]
        self.items[0].prev = self.items[-1]
        self.items[-1].next = self.items[0]
        self.current = self.find((self.x, self.y))

    def find(self, pos):

        items = [ item for item in self.items if item.x == pos[0] and item.y == pos[1] ]
        assert len(items) <= 1, 'dups in list?'
        return items[0] if len(items) == 1 else None

class FlatMap(BaseMap):

    def __init__(self, mapp, pos):

        self.mapp = mapp
        self.x, self.y = pos[0]
        self.heading = pos[1]

        # create the list of items
        self.items = self.get_items(mapp)
        self.link_items()

    def get_items(self, mapp):
        if self.heading in [ '>', '<' ]:
            return [ Item(x, self.y, v) for x, v in enumerate(mapp[self.y]) if v != ' ' ]
        else:
            return [ Item(self.x, y, r[self.x]) for y, r in enumerate(mapp) if r[self.x] != ' ' ]

    def next(self):

        moved = False

        if self.heading in [ '>', 'v' ]:
            if self.current.next.v != '#':
                self.current = self.current.next
                moved = True
        else:
            if self.current.prev.v != '#':
                self.current = self.current.prev
                moved = True

        return moved

    def calc_turn(self, pos, turn):

        turns = {
            '^': { 'L': '<', 'R': '>' },
            'v': { 'L': '>', 'R': '<' },
            '>': { 'L': '^', 'R': 'v' },
            '<': { 'L': 'v', 'R': '^' },
        }

        if not turn: return self.heading 
        new_heading = turns[self.heading][turn]
        log.debug(f'calculating turn direction for {self.current} with heading {self.heading} to {new_heading}')
        return new_heading

class CubeMap(BaseMap):

    axes = {
        'x': { 'sides': [ 'front', 'right', 'back', 'left' ], 'rotations': [ 0, 0, 0, 0], 'reversed': [ False, False, False, False] },
        'y': { 'sides': [ 'top', 'right', 'bottom', 'left' ], 'rotations': [ 0, 3, 2, 1], 'reversed': [ False, False, True, True] },
        'z': { 'sides': [ 'top', 'front', 'bottom', 'back' ], 'rotations': [ 0, 0, 0, 2], 'reversed': [ False, False, True, False] }
    }

    def __init__(self, mapp, pos):

        self.mapp = mapp
        self.x, self.y = pos[0]
        self.heading = pos[1]

        self.sides = parse_sides(self.mapp)
        self.sidelen = self.sides['top'].sidelen

        # start by figuring out which side we're on and the direction of
        # travel (forward or reverse) to determine the axis of the cube to traverse
        side = self.calc_side(self.x, self.y)
        starting_side = side.name
        self.axis = self.calc_axis(side.name, self.heading)
        self.forward = side.is_forward(self.axis, self.heading)

        # rotate the sides so that they are aligned on the axis
        sides = []
        for ix, name in enumerate(self.axes[self.axis]['sides']):
            rot = self.axes[self.axis]['rotations'][ix]
            curr_side = self.sides[name]
            pp = curr_side.rotate(curr_side.points, rot)
            sides.append(pp)

        # get the row and col offset of the initial point. that will be relevant
        # when translating the path to other sides of the cube
        for side in sides:
            offsets = [ (x, y) for x in range(self.sidelen) for y in range(self.sidelen) if side[y][x] == (self.x, self.y) ]
            if len(offsets) == 1:
                col_offset, row_offset = offsets[0]
                break
        log.trace(f'offsets for path: row_offset: {row_offset}, col_offset: {col_offset}')

        # create the list of items
        points = []
        for ix, name in enumerate(self.axes[self.axis]['sides']):
            side = sides[ix]
            if self.axis in ['x', 'y']:
                ii = [ side[row_offset][i] for i in range(self.sidelen) ]
            else:
                ii = [ side[i][col_offset] for i in range(self.sidelen) ]

            if self.axes[self.axis]['reversed'] == True:
                ii = list(reversed(ii))
    
            curr_side.print(side)
            log.trace(ii)
            log.trace('')

            points.extend(ii)

        self.items = [ Item(p[0], p[1], self.mapp[p[1]][p[0]]) for p in points ]
        self.link_items()

        log.debug(f'  pos: {self.x},{self.y}')
        log.debug(f'  travelling {"forward" if self.forward else "backward"} on the {self.axis} axis of {starting_side} in the {self.heading} direction')
        log.debug(f'  row_offset: {row_offset}, col_offset: {col_offset}')
        log.debug(f'  current: {self.current}')
        log.debug('')
        
    def calc_side(self, x, y):
        X = x // self.sidelen
        Y = y // self.sidelen
        sides = [ s for s in self.sides.values() if s.position == (X, Y) ]
        assert len(sides) == 1, f'cannot find a side for {X},{Y}'
        return sides[0]

    def calc_axis(self, side, heading):

        axis = None
        if heading in [ '<', '>' ]:
            if side in [ 'left', 'right', 'front', 'back' ]:
                axis = 'x'
            elif side in [ 'top', 'bottom' ]:
                axis = 'y'
        elif heading in [ '^', 'v' ]:
            if side in [ 'top', 'front', 'bottom', 'back' ]:
                axis = 'z'
            elif side in [ 'left', 'right' ]:
                axis = 'y'

        return axis

    def next(self):

        moved = False

        if self.forward:
            if self.current.next.v != '#':
                self.current = self.current.next
                moved = True
        else:
            if self.current.prev.v != '#':
                self.current = self.current.prev
                moved = True

        return moved

    def calc_turn(self, pos, turn):

        turns = {
            '^': { 'L': '<', 'R': '>' },
            'v': { 'L': '>', 'R': '<' },
            '>': { 'L': '^', 'R': 'v' },
            '<': { 'L': 'v', 'R': '^' },
        }

        if not turn: return self.heading 

        # calculate the side that the current point is on. we don't care
        # about proper rotation here, just what side the current point is on
        log.debug(f'  calculating new heading for {pos}')
        for side in self.sides.values():
            offsets = [ (x, y) for x in range(self.sidelen) for y in range(self.sidelen) if side.points[y][x] == (pos.x, pos.y) ]
            if len(offsets) == 1: break
         
        log.debug(f'  current point is on {side.name}, travel is forward={self.forward}, turning {turn}')
        return side.calc_turn(self.axis, self.forward, turn)



def test_flat_map(mapp):

    data = {
        (((8, 0), '>'), 5),
        (((4, 5), 'v'), 5),
    }

    for pos, num_steps in data:

        log.debug(f'testing {num_steps} in each direction from {pos}')

        path = FlatMap(mapp, pos)
        steps = [ (p.x, p.y) for p in path.items ]
        stepstr = ', '.join([ f'({s[0]:02},{s[1]:02})' for s in steps ])
        symbols = ''.join([ mapp[step[1]][step[0]] for step in steps ])
        log.info(f'{pos}: {stepstr}: {symbols}')

def test_cube_map(mapp):

    data = [
        (((8, 0), '>'), [ (5, 'R'), (2, 'L'), (5, None) ], ((14, 9), 'v')),
#       (((0, 4), '<'), 20),
#       (((8, 4), 'v'), 20),
#       (((15, 8), 'v'), 20),
#       (((8, 0), 'v'), 20),
#       (((14, 10), 'v'), 20),
#       (((6, 5), '^'), 20),
    ]

    for start, steps, end in data:
        curr = start
        log.info(f'moving {steps} starting at {start}:')
        for num_steps, turn_dir in steps:
            log.debug(f'-------')
            log.debug(f'moving {num_steps} steps heading {curr[1]} from {curr[0]} then turning {turn_dir}')
            path = CubeMap(mapp, curr)
            for i in range(num_steps):
                moved = path.next()
                if moved:
                    log.debug(f'  new position: {path.current}')
                else:
                    log.debug(f'  path blocked at {path.current}')
#                   break

            old_heading = curr[1]
            new_heading = path.calc_turn(path.current, turn_dir)
            log.debug(f'reached destination for this leg at {path.current}. turning {turn_dir} from old heading {old_heading} to {new_heading}')
            log.debug(f'')
            curr = ((path.current.x, path.current.y), new_heading)
        if start != end:
            log.failure(f'  expected: {end}, got {curr}')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=f"Jungle Map Test")
    parser.add_argument('-t', '--testing', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('-vv', '--trace', action='store_true', default=False)
    cmdline = parser.parse_args()

    log.context.debug = cmdline.verbose or cmdline.trace
    log.context.trace = cmdline.trace
    log.info(f'log.context.debug: {log.context.debug}')

    mapp = []
    filename = './input-test' if cmdline.testing else './input'
    with open('./input-test', 'r') as infile:
        for l in [ l.rstrip() for l in infile ]:
            if len(l) == 0: break
            mapp.append(l)

        map_width = max(set([ len(l) for l in mapp ]))
        mapp = [ (l + (' '*map_width))[0:map_width] for l in mapp ]

#   test_flat_map(mapp)
    test_cube_map(mapp)


