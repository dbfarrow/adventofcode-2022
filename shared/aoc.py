#!/usr/bin/env python
import sys
import argparse
from shared import log

class __AOC:

    def __init__(self, day=0, year=2020):
        assert day >= 0, "please set the day for the challenge"
        self.day = day
        self.year = year

    def parse_cmdline(self):
        
        parser = argparse.ArgumentParser(description=f"AdventOfCode {self.year} - day {self.day}")
        parser.add_argument('-t', '--testing', action='store_true', default=False)
        parser.add_argument('-v', '--verbose', action='store_true', default=False)
        parser.add_argument('-vv', '--trace', action='store_true', default=False)
        parser.add_argument('-p', '--part')
        self.parse_cmdline_extra(parser)
        self.cmdline = parser.parse_args()

        log.context.debug = self.cmdline.verbose or self.cmdline.trace
        log.context.trace = self.cmdline.trace
        log.info(f'log.context.debug: {log.context.debug}')

    def parse_cmdline_extra(self, parser):
        return

    def get_input(self):

        filename = "./input" if not self.cmdline.testing else "./input-test"
        with open(filename, "r") as infile:
            return [ l.rstrip() for l in infile ]

    def do_part(self, part):
        if not self.cmdline.part or self.cmdline.part == part:
            return True
        else:
            return False

    def A(self):
        return None

    def B(self):
        return None

    def run(self):
        self.parse_cmdline()

        if self.do_part('a'): 
            log.info(f"AdventOfCode {self.year} - day {self.day} part A")
            a = self.A()
            log.success(a) if a else log.failure('not implemented')

        if self.do_part('b'): 
            log.info(f"AdventOfCode {self.year} - day {self.day} part B")
            b = self.B()
            log.success(b) if b else log.failure('not implemented')

if __name__ == "__main__":

    __AOC().run()

