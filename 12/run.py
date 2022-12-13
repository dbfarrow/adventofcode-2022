#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
import json
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=12)

    def find_point(self, mapp, pt):
        for y, r in enumerate(mapp):
            if pt in r:
                x = r.rfind(pt)
                if x >= 0:
                    return (x, y)
                break

        return None 

    def is_acceptable_move(self, mapp, src, dest):

        src_alt = self.get_altitude(mapp, src)
        dest_alt = self.get_altitude(mapp, dest)

        diff = ord(dest_alt) - ord(src_alt)
        acceptable = (diff <= 1)
        return acceptable
        
    def get_altitude(self, mapp, pt):
        return mapp[pt[1]][pt[0]]

    def get_neighbors(self, mapp, pt):
        
        neighbors = []
        x = pt[0]
        y = pt[1]
        max_x = len(mapp[0])
        max_y = len(mapp)

        for dest in [ (x, y-1), (x, y+1), (x-1, y), (x+1, y) ]:
            if (dest[0] >= max_x) or (dest[1] >= max_y) or (dest[0] < 0) or (dest[1] < 0): continue
            if self.is_acceptable_move(mapp, (x, y), dest):
                neighbors.append(dest)

        return neighbors
        
    def shortest_path(self, mapp, start, end):
        
        mapp[start[1]] = mapp[start[1]].replace('S', 'a')
        mapp[end[1]] = mapp[end[1]].replace('E', 'z')
        visited = []
        moves = [[ start ]]

        if start == end:
            return []

        while moves:
            path = moves.pop(0)
            node = path[-1]
       
            if node not in visited:
                neighbors = self.get_neighbors(mapp, node)
                for n in neighbors:
                    new = list(path)
                    new.append(n)
                    moves.append(new)

                    if n == end:
#                       for p in new:
#                           log.info(p)
                        return len(new) - 1

                visited.append(node)

        return 0

    def find_lowest_points(self, mapp):

        points = []
        for y, r in enumerate(mapp):
            for x, h in enumerate(r):
                if h == 'a':
                    points.append((x, y))
        return points

    def A(self):
        
        mapp = self.get_input()
        start = self.find_point(mapp, 'S')
        end = self.find_point(mapp, 'E')
        log.info(f'searching for shortest path between {start} and {end}')
        return self.shortest_path(mapp, start, end)

    def B(self):

        mapp = self.get_input()
        end = self.find_point(mapp, 'E')
        lengths = [ l for l in [ self.shortest_path(mapp, p, end) for p in self.find_lowest_points(mapp) ] if l > 0 ]
        return min(lengths)


if __name__ == "__main__":
    AOC().run()
