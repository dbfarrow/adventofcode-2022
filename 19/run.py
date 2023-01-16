#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from copy import copy
import json
import math
import re
from shared.aoc import __AOC
from shared import log

class Blueprint:

    precedence = [ 'geode', 'obsidian', 'clay', 'ore' ]

    def __init__(self, bpspec):
        
        self.id, robotspec = bpspec.split(': ')
        robotspec = robotspec.split('. ')

        self.robots = defaultdict(dict)
        self.maxes = defaultdict(int)

        for robot in robotspec:
            rpat = 'Each (.*) robot costs ([^\.]+)'
            m = re.match(rpat, robot)
            if m:
                rtype = m.group(1)
                costspecs = m.group(2).split(' and ')
                for c in costspecs:
                    number, units = c.split(' ')
                    self.robots[rtype][units] = int(number)
                    self.maxes[units] = max(int(number), self.maxes[units])                

        # we can never have enough geode breaking robots
        self.maxes['geode'] = math.inf

    def __repr__(self):
        return f'{self.id}: robots: {self.robots}, maxes: {self.maxes}'

class State:

    def __init__(self, bp, t, tobuild, robots={}, resources={}):

        self.bp = bp
        self.t = t
        self.tobuild = tobuild

        self.robots = defaultdict(dict)
        self.robots.update({ 'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0 })
        self.robots.update(robots)

        self.resources = defaultdict(dict)
        self.resources.update({ 'ore': 0, 'obsidian': 0, 'clay': 0, 'geode': 0 })
        self.resources.update(resources)

    def __repr__(self):
        return f'time: {self.t:02}, built: {self.tobuild}, bp.id: {self.bp.id}, robots: {json.dumps(self.robots)}, resources: {json.dumps(self.resources)}'

    def hash(self):
        return str(self)

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=19)

    def get_input(self):
        return [ Blueprint(d) for d in super().get_input() ]

    def build_time(self, state, cost, rtype):
        return max(0, math.inf if state.robots[rtype] == 0 else math.ceil((cost[rtype] - state.resources[rtype]) / state.robots[rtype]))

    def run_blueprint(self, bp, duration):

        states = [ State(bp, 0, None, { 'ore': 1 }) ]
        max_geodes = 0

        # at each state we want to calculate what the set of next possible (and reasonable) states are
        # and keep track of which state yields the highest number of cracked geodes.
        #
        # from each state, we calculate how long it will take to create each type of robot and calculate
        # a new state based on having waited the amount of time necessary to make that type of robot. the
        # new state will reflect the time waited and the amount of material mined during the wait as well
        # as the updated inventory of robots after building the new robot
        for state in states:

            for rtype in [ rtype for rtype in bp.robots ]:

                # if we already have enough of these robots to cover the max cost to
                # build any other robot, we don't need to make any more
                if state.robots[rtype] >= bp.maxes[rtype]: continue

                # calculate how long it will take to make a robot of this type
                cost = bp.robots[rtype]
                build_time = max([ self.build_time(state, cost, rt) for rt in cost ])

                resources = { rt: state.resources[rt] + ((build_time + 1) * state.robots[rt]) - cost.get(rt,0) for rt in state.robots }
                robots = copy(state.robots)
                robots[rtype] += 1
                ns = State(bp, state.t + build_time + 1, rtype, robots, resources)

                # don't continue if this state occurs after the max time
                if ns.t >= duration: continue

                # check to see if we have a new expected max number of geodes cracked
                remaining = duration - ns.t
                max_geodes = max(max_geodes, ns.resources['geode'] + (ns.robots['geode'] * remaining))

                # if this state were to be capable of buildin a new geode robot
                # each minute from here on out, could it possibly crack more
                # geodes than the current max? if not, then we don't need to 
                # see where this path leads
                max_possible = ns.resources['geode'] + (remaining*(remaining - 1))/2 + (remaining * ns.robots['geode'])
                if max_possible < max_geodes: continue

                # at this point, there is reason to believe this state may be on the optimal path. save it to the
                # states list for further processing
                states.append(ns)

        log.info(f'  max_geodes: {max_geodes}')
        return max_geodes

    def A(self):
        best = [ self.run_blueprint(bp, 24) for bp in self.get_input() ]
        return sum([ (ix + 1) * b for ix, b in enumerate(best) ])

    def B(self):
        best = [ self.run_blueprint(bp, 32) for bp in self.get_input()[0:3] ]
        score = 1
        for ix, b in enumerate(best):
            log.info(f'  {ix}: {b}')
            score *= b
        return score

if __name__ == "__main__":
    AOC().run()
