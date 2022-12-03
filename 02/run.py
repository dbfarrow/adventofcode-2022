#!/usr/bin/env python3
import sys
sys.path.append('..')

from shared.aoc import __AOC
from shared import log

rock = 1
paper = 2
scissors = 3

win = 6
lose = 0
draw = 3

opponent = { 'A': rock, 'B': paper, 'C': scissors }
player = { 'X': rock, 'Y': paper, 'Z': scissors }
outcome = { 'X': lose, 'Y': draw, 'Z': win }

games = {
    (rock, rock, draw),
    (rock, paper, win),
    (rock, scissors, lose),
    (paper, rock, lose),
    (paper, paper, draw),
    (paper, scissors, win),
    (scissors, rock, win),
    (scissors, paper, lose),
    (scissors, scissors, draw)
}

def parser_a(s):
    parts = s.split(' ')
    return (opponent[parts[0]], player[parts[1]])

def parser_b(s):
    parts = s.split(' ')
    return (opponent[parts[0]], outcome[parts[1]])

class AOC(__AOC):

    def __init__(self):
        super().__init__(day=2)

    def get_input(self, parser):
        return map(parser, super().get_input())

    def A(self):
        lookup = { (g[0], g[1]): g[2] for g in games }      # (opponent's play, player's play): outcome
        return sum([ p[1] + lookup[p] for p in list(self.get_input(parser_a)) ])    # player's play + outcome

    def B(self):
        lookup = { (g[0], g[2]): g[1] for g in games }      # (oppenent's play, outcome): player's play
        return sum([ p[1] + lookup[p] for p in list(self.get_input(parser_b)) ])    # outcome + player's play

if __name__ == "__main__":
    AOC().run()
