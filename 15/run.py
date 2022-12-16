#!/usr/bin/env python3
import sys
sys.path.append('..')

import re
from shared.aoc import __AOC
from shared import log

def calc_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def calc_overlap(sensor, target_row):

    overlap = {}

    dx = sensor.dist - abs(sensor.sensor[1] - target_row) + 1
    for i in range(dx):
        overlap[sensor.sensor[0]+i, target_row] = '#'
        overlap[sensor.sensor[0]-i, target_row] = '#'

    # mark the beacon if it's in the target row
    if sensor.beacon[1] == target_row: overlap[sensor.beacon] = 'B'

    log.debug(f'{sensor}; target_row = {target_row}; overlap: {overlap}')
    return overlap

class Sensor:

    def __init__(self, data):
        
        p = 'Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)'
        m = re.match(p, data)
        assert m, 'failed to parse: {data}'
        self.location = (int(m.group(1)), int(m.group(2)) )
        self.beacon = (int(m.group(3)), int(m.group(4)) )
        self.dist = calc_distance(self.location, self.beacon)

    def __repr__(self):
        return f'sensor: ({self.sensor[0]: 4}, {self.sensor[1]: 4}); beacon: ({self.beacon[0]: 4}, {self.beacon[1]: 4}); distance: {self.dist}'

    def get_row_overlap(self, row):

        # there is no row overlap if the sensor location is further away than the sensor's closest beacon
        dy = abs(self.location[1] - row) 
        if dy > self.dist: return None

        # if there is overlap it will be left and right of the sensor's x location in the amount of 
        # the difference between the distance between the sensor and its beacon and the sensor and the 
        # line of interest
        dx = self.dist - dy
        return [ self.location[0] - dx, self.location[0] + dx ]

def take_first(e):
    return e[0]

def merge_ranges(ranges):
    log.debug(ranges)
    x = [ ranges.pop(0) ]
    for r in ranges:
        if r[0] > (x[-1][1] + 1):
            log.debug(f'{r} doesn\'t overlap {x[-1]}')
            x.append(r)
        elif r[1] > x[-1][1]:
            log.debug(f'extending {x[-1]} with {r}')
            x[-1][1] = r[1]
            log.debug(f'   {x[-1]}') 
        else:
            log.debug(f'{r} falls within {x[-1]}')

    return x

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=15)

    def A(self):

        target_row = 10 if self.cmdline.testing else 2000000
        sensors = [ Sensor(i) for i in self.get_input() ]
        ranges = sorted([ s for s in [ s.get_row_overlap(target_row) for s in sensors ] if s ], key=take_first)
        merged = merge_ranges(ranges)
        assert len(merged) == 1, 'not expecting gap in ranges on row {target_row}'
        return merged[0][1] - merged[0][0]

    def B(self):

        max_y = 20 if self.cmdline.testing else 4000000
        sensors = [ Sensor(i) for i in self.get_input() ]
        for i in range(max_y):
            ranges = sorted([ s for s in [ s.get_row_overlap(i) for s in sensors ] if s ], key=take_first)
            merged = merge_ranges(ranges)
            if len(merged) > 1:
                break

        log.info(f'{i:02}: {merged}')
        x1 = merged[0][1]
        x2 = merged[1][0]
        assert x2 - x1 == 2, 'unexpected gap size'
        return (4000000 * (x1 + 1)) + i

if __name__ == "__main__":
    AOC().run()
