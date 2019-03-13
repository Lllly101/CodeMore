#! /usr/bin/env python3
"""
R = (A * Rn-1 + C) % M
"""

class PRNG():
    a =  2**32
    c = 1
    m = 22695477
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

if __name__ == "__main__":
    prng = PRNG(1013904223)

    counts = 0
    while True:
        print(prng.next())
        counts += 1
        if counts >= 10:
            break