#!/usr/bin/env python3
import sys
sys.path.append('..')

from collections import defaultdict
from itertools import permutations
import re
from shared.aoc import __AOC
from shared import log

class Node():
    
    def __init__(self, data):

        p = 'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z, ]+)'
        m = re.match(p, data)
        assert m != None, f'failed to parse: {data}'
    
        self.name = m.group(1)
        self.rate = int(m.group(2))
        self.neighbors = [ s.strip() for s in m.group(3).split(',') ]
        self.open = False

    def __repr__(self):
        return f'{self.name}: rate = {self.rate:02}; neighbors: {",".join(self.neighbors)}'
        
class Graph:

    def __init__(self, nodes):

        self.nodes = { n.name: n for n in nodes }
        self.graph = defaultdict(list)
        for node in nodes:
            for n in node.neighbors:
                self.graph[node].append(self.nodes[n])
                self.graph[self.nodes[n]].append(node)
       
    def __repr__(self):
        r = ''
        for k, v in self.graph.items():
            r += f'  {k}: {v}\n'
        return r

    def print_matrix(self, m):
    
        header = ''.join([ f'{h:6}'for h in m[list(m.keys())[0]] ])
        log.debug('        ' + header)

        for i in m:
            row = f'{i}: '
            for j in m[i]:
                row += f'{m[i][j]: 6}' 
            log.debug(row)

    def shortest_paths(self):

        a = defaultdict(dict)
        names = list(self.nodes.keys())
        for i in names:
            for j in names:
                a[i][j] = 1 if ((i != j) and (self.nodes[j].name in self.nodes[i].neighbors)) else float('inf')

        for k in names:
            for i in names:
                for j in names:
                    if i == j: continue
                    new_shortest = a[i][k] + a[k][j]
                    if a[i][j] > new_shortest:
                        a[i][j] = new_shortest

        return a

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=16) 
        self.cache = {}
        self.valve_bits = None

    def path_to_bitmap(self, valves, path):

        if not self.valve_bits: 
            self.valve_bits = { v: ix for ix, v in enumerate(valves) }

        bitmap = 0
        for p in path:
            if p == 'AA': continue
            bitmap += 1 << self.valve_bits[p]

        return bitmap

    def get_paths(self, data, deadline):

        graph = Graph([ Node(i) for i in data ])

        # calculate the shortest paths between any pairs of nodes
        sps = graph.shortest_paths()

        # get a list of the valves that can contribute non-zero flow
        valves = [ n for n in graph.nodes if graph.nodes[n].rate > 0 ]

        # starting from 'AA' visit every possible combination of paths
        # through non-zero flow valves stopping when visiting a valve
        # will take more time than we have. for each node we visit, append
        # the path to every neighbor that contributes a non-zero flow if we 
        # can get there before time expires. 
        #
        # each item in the paths  array has the following contents:
        # [ node, valves_visited, time_remaining, total_flow, bitmap ]
        paths = [ ('AA', [ 'AA' ], deadline, 0, self.path_to_bitmap(valves, [ 'AA' ])) ]
        for curr_node, curr_visited, remaining, valve_total, bitmap in paths:

            # add an item to paths for each non-zero flow neighbor
            # that we haven't already visited
            for valve in valves:
                if valve in curr_visited: continue
                dist = sps[curr_node][valve]

                # the amount of time the valve releases pressure is equal to the number
                # of minutes left time the valve flow rate. release time is calculated
                # as the time remaining minus travel time to the valve minus one 
                # minute to open it
                release_time = remaining - dist - 1

                # if the release time is less than or equal to 0, don't bother
                if release_time <= 0: continue

                next_path = curr_visited + [ valve ]
                bitmap = self.path_to_bitmap(valves, next_path)
                p = (valve, curr_visited + [ valve ], release_time, valve_total + (release_time * graph.nodes[valve].rate), bitmap)
                paths.append(p)
            
        return paths 

    def A(self):
        paths = self.get_paths(self.get_input(), 30)
        return max([ p[3] for p in paths ])

    def B(self):

        paths = self.get_paths(self.get_input(), 26)
        best = 0

        log.info(f'found: {len(paths)} paths')
        ix = 0
        for node_a, visited_a, remaining_a, valve_total_a, bitmap_a in paths:
            for node_b, visited_b, remaining_b, valve_total_b, bitmap_b in paths:
                if bitmap_a & bitmap_b == 0:
                    log.debug(f'no overlap: {visited_a} - {visited_b}: {bitmap_a} & {bitmap_b}')
                    best = max(best, valve_total_a + valve_total_b)
        
            ix += 1
            if ix % 1000 == 0:
                log.info(f'completed {ix} outer loop iterations')
        return best

if __name__ == "__main__":
    AOC().run()
