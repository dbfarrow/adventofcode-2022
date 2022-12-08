#!/usr/bin/env python3
import sys
sys.path.append('..')

from functools import reduce
from shared.aoc import __AOC
from shared import log

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=8)

    def is_visible(self, forest, coord):
        x = coord[0]
        y = coord[1]
        point = forest[y][x]

        # check left
        row = forest[y]
        col = [ row[x] for row in forest ]
        visibility = [
            max(row[0:x]) < point,     # from the left
            max(row[x+1:]) < point,     # from the right
            max(col[0:y]) < point,     # from the top
            max(col[y+1:]) < point      # from the bottom
        ]
#       log.info(f'is {coord} = {point} visible? {visibility}')
        return visibility 

    def A(self):
        forest = self.get_input()
        assert len(forest) == len(forest[0]), 'input is not square'
        coords = [ (i, j) for j in range(1, len(forest) - 1) for i in range(1, len(forest) - 1)] 
        visibility = [ self.is_visible(forest, c) for c in coords ]
        visible = ((len(forest) * 4) - 4) + sum([ any(v) for v in visibility ])
#       log.info(visibility)
#       log.info(visible)
        return visible

    def calc_view_distance(self, trees, height):
        distance = 0
        for i in range(0, len(trees)):
            if trees[i] < height:
                distance += 1
            else:
                distance += 1
                break
    
#       log.info(f'trees: {trees}, height: {height}, distance: {distance}')
        return distance

    def scenic_score(self, forest, coord):
        x = coord[0]
        y = coord[1]
        height = forest[y][x]
        row = [ c for c in forest[y] ]
        row = forest[y]
        col = [ row[x] for row in forest ]
    
#       log.info(f'{coord}: {row}')
        distances = [
            self.calc_view_distance(list(reversed(col[0:y])), height),   # looking up
            self.calc_view_distance(list(reversed(row[0:x])), height),   # looking left
            self.calc_view_distance(list(row[x+1:]), height),            # looking right
            self.calc_view_distance(list(col[y+1:]), height),            # looking down
        ]
        score = reduce((lambda x, y: x * y), distances)
#       log.info(f'{coord}={height}: distances: {distances}, score: {score}')
#       log.info('')
        return score
    
    def B(self):
        forest = self.get_input()
        assert len(forest) == len(forest[0]), 'input is not square'
        coords = [ (i, j) for j in range(1, len(forest) - 1) for i in range(1, len(forest) - 1)] 
        return max([ self.scenic_score(forest, c) for c in coords ])
        
if __name__ == "__main__":
    AOC().run()
