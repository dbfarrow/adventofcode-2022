#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from sides import parse_sides
from shared import log

def rotate_heading(heading, count):

    headings = [ '<', '^', '>', 'v' ]
    offset = headings.index(heading)
    return headings[(offset + count) % 4]        

#
# Items are used by the CubeMap Sides to represent the x, y coordinates and value at that
# location in the source data file. For example, in the test data set, the top left corner 
# (coord 0,) of the top surface of the cube hold the item ((8, 0), '.') 
#
class Item:

    def __init__(self, x, y, v):

        self.x = x
        self.y = y
        self.v = v
        self.next = None
        self.prev = None

    def __repr__(self):
        return f'({self.x},{self.y}): {self.v}'

class BaseMap:

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

    def unrotate(self, pos):
        log.info('unrotate means nothing to me')
        return pos

class FlatMap(BaseMap):

    def __init__(self, mapp, pos):

        self.mapp = mapp
        self.x, self.y = pos[0]
        self.heading = pos[1]

        # create the list of items and link them together
        if self.heading in [ '>', '<' ]:
            self.items = [ Item(x, self.y, v) for x, v in enumerate(mapp[self.y]) if v != ' ' ]
        else:
            self.items = [ Item(self.x, y, r[self.x]) for y, r in enumerate(mapp) if r[self.x] != ' ' ]
        self.link_items()

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

        if not turn: return self.heading 
        return rotate_heading(self.heading, 1 if turn == 'R' else -1)

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
        rotated_sides = []
        for ix, name in enumerate(self.axes[self.axis]['sides']):
            rot = self.axes[self.axis]['rotations'][ix]
            curr_side = self.sides[name]
            pp = curr_side.rotate(curr_side.points, rot)
            rotated_sides.append(pp)

        # get the row and col offset of the initial point. that will be relevant
        # when translating the path to other sides of the cube. there is certainly
        # a more efficient way of finding this but i ran out of energy before
        # optimizing this
        for rotated in rotated_sides:
            offsets = [ (x, y) for x in range(self.sidelen) for y in range(self.sidelen) if rotated[y][x] == (self.x, self.y) ]
            if len(offsets) == 1:
                col_offset, row_offset = offsets[0]
                break
        log.trace(f'offsets for path: row_offset: {row_offset}, col_offset: {col_offset}')

        # create the list of points on the axis
        points = []
        for ix, name in enumerate(self.axes[self.axis]['sides']):
            side = rotated_sides[ix]
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

        # then turn the list of points into Item objects and link them together
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

        if not turn: return self.heading 

        # calculate the side that the current point is on. we don't care
        # about proper rotation here, just what side the current point is on
        side = self.calc_side(pos.x, pos.y)
        log.debug(f'  current point is on {side.name}, travel is forward={self.forward}, turning {turn}')
        return side.calc_turn(self.axis, self.forward, turn)

    def unrotate(self, pos):
        side = self.calc_side(pos[0][0], pos[0][1])
        return (pos[0], rotate_heading(pos[1], -side.rotation))
