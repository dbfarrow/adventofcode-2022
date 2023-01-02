#!/usr/bin/python3

class Item:

    def __init__(self, x, y, v):

        self.x = x
        self.y = y
        self.v = v
        self.next = None
        self.prev = None

    def __repr__(self):
        return f'({self.x},{self.y}): {self.v}'


