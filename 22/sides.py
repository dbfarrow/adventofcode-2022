#!/usr/bin/python3
import sys
sys.path.append('..')

from shared import log
from collections import defaultdict


class NoDataException(Exception):
    def __init__(self, position): self.position = position


cube_sides = None
        
def parse_sides(mapp):

    global cube_sides
    if cube_sides != None:
        return cube_sides

    dim = (len(mapp[0]), len(mapp))
    parse_map = {
        (16,12): {
            0: [ None, None, (Top, 0), None ],
            1: [ (Back, 0), (Left, 0), (Front, 0), None ],
            2: [ None, None, (Bottom, 0), (Right, -1) ]
        },
        (150,200): {
            0: [ None, (Top, 0), (Right, 1) ],
            1: [ None, (Front, 0), None ],
            2: [ (Left, 1), (Bottom, 0), None ],
            3: [ (Back, 1), None, None ]
        },
    }

    cube_sides = {}
    nrows, ncols = (3, 4) if dim == (16,12) else (4, 3)
    
    sidelen = dim[0] // ncols
    for y in range(nrows):
        for x in range(ncols):
            spec = parse_map[dim][y][x]
            if spec:
                cls, rot = spec
                side = cls(mapp, dim, (x, y), sidelen)
                if rot != 0:
                    side.points = side.rotate(side.points, rot)
                    side.rotation = rot
                cube_sides[side.name] = side
                side.print()
 
    return cube_sides


class Side:

    def __init__(self, mapp, dim, position, sidelen):
        
        self.mapp = mapp
        self.dim = dim
        self.name = self.__class__.__name__.lower()
        self.position = position
        self.sidelen = sidelen
        self.rotation = 0

        X = self.position[0]
        Y = self.position[1]

        self.points = defaultdict(dict)
        for i in range(sidelen):
            for j in range(sidelen):
                xx = (X * sidelen) + j
                yy = (Y * sidelen) + i
                if mapp[yy][xx] == ' ': raise NoDataException(position)
                self.points[i][j] = (xx, yy)

    def print(self, points=None):
        log.trace(f'side {self.name}, position: {self.position}:')

        if points == None: points = self.points
        for y, r in points.items():
            coords = ''
            vals = ''
            for x, v in r.items():
                xx, yy = points[y][x]
                coords += f'({xx:02},{yy:02}) '
                vals += self.mapp[yy][xx]
            log.trace(f'  {coords}:    {vals}')

        log.trace('')

    def is_forward(self, axis, heading):
        # in most cases, a heading of > or v indicates forward/clockwise
        # travel around the axis. however, that is not always the case 
        # and depends entirely on the face of the cube that travel started 
        # because some faces are rotated when you are traversing them.
        log.debug(f'doot: is_forward: name: {self.name}, axis: {axis}, heading: {heading}')
        return heading in [ '>', 'v' ]

    def rotate(self, points, count):

#       log.trace(f'rotating side by {count} places')
#       self.print(points)

        for n in range(count % 4):
            np = defaultdict(dict)
            for x in range(self.sidelen):
                for y in range(self.sidelen):
                    xx = y
                    yy = self.sidelen - x - 1
                    np[y][x] = points[yy][xx]
            points = np

#           log.trace(f'  step: {n}')
#           self.print(points)

        return points

    def calc_turn(self, axis, moving_forward, turn):
        log.debug(f'doot: calc_turn: name: {self.name}, axis: {axis}, moving_forward: {moving_forward}, turn: {turn}')
        return self.turns[(axis, moving_forward)][turn]
            

class Top(Side):

    turns = {
        ( 'y', True): { 'L': '^', 'R': 'v' },
        ( 'y', False): { 'L': 'v', 'R': '^' },
        ( 'z', True): { 'L': '>', 'R': '<' },
        ( 'z', False): { 'L': '<', 'R': '>' },
    }

class Bottom(Side):

    turns = {
        ( 'y', True): { 'L': 'v', 'R': '^' },
        ( 'y', False): { 'L': '^', 'R': 'v' },
        ( 'z', True): { 'L': '>', 'R': '<' },
        ( 'z', False): { 'L': '<', 'R': '>' },
    }

    def is_forward(self, axis, heading):
        # on the bottom, the direction of travel indicated by 
        # left and right on the z axis are reversed
        forward = super().is_forward(axis, heading)
        if axis == 'y':
            forward = not forward
        return forward


class Left(Side):

    turns = {
        ( 'x', True): { 'L': '^', 'R': 'v' },
        ( 'x', False): { 'L': 'v', 'R': '^' },
        ( 'y', True): { 'L': '<', 'R': '>' },
        ( 'y', False): { 'L': '>', 'R': '<' },
    }

    def is_forward(self, axis, heading):
        # on the left, the direction of travel indicated by 
        # up and down on the y axis are reversed
        forward = super().is_forward(axis, heading)
        if axis == 'y' and heading in [ '^', 'v' ]:
            forward = not forward
        return forward

class Right(Side):

    turns = {
        ( 'x', True): { 'L': '^', 'R': 'v' },
        ( 'x', False): { 'L': 'v', 'R': '^' },
        ( 'y', True): { 'L': '>', 'R': '<' },
        ( 'y', False): { 'L': '<', 'R': '>' },
    }

class Front(Side):

    turns = {
        ( 'x', True): { 'L': '^', 'R': 'v' },
        ( 'x', False): { 'L': 'v', 'R': '^' },
        ( 'z', True): { 'L': '>', 'R': '<' },
        ( 'z', False): { 'L': '<', 'R': '>' },
    }

class Back(Side):

    turns = {
        ( 'x', True): { 'L': '^', 'R': 'v' },
        ( 'x', False): { 'L': 'v', 'R': '^' },
        ( 'z', True): { 'L': '<', 'R': '>' },
        ( 'z', False): { 'L': '>', 'R': '<' },
    }

    def is_forward(self, axis, heading):
        forward = super().is_forward(axis, heading)
        if axis == 'z':
            forward = not forward
        return forward

