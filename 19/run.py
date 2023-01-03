#!/usr/bin/env python3
import sys
sys.path.append('..')

import json
import re
from shared.aoc import __AOC
from shared import log

class Blueprint:

    def __init__(self, name, cost):

        self.name = name
        cost = cost.split(' and ')
        self.cost = {}
        for c in cost:
            number, units = c.split(' ')
            self.cost[units] = number

    def __repr__(self):
        return f'{self.name}: {self.cost}'

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=19)

    def parse_blueprint(self, ix, d):

        parts = d.split(': ')
        robots = parts[1].split('. ')
        bp = []
        for r in robots:
            pattern = 'Each (.*) robot costs (.*)'
            m = re.match(pattern, r)
            if m:
                bp.append(Robot(m.group(1), m.group(2)))
                
        return bp

    def get_input(self):

        blueprints = []
        data = super().get_input()
        for ix, d in enumerate(data):
            blueprints.append(self.parse_blueprint(ix, d))

        return blueprints

    def A(self):
        blueprints = self.get_input()
        log.info(json.dumps(blueprints, default=str, indent=2))
        return None

    def B(self):
        return None

if __name__ == "__main__":
    AOC().run()
