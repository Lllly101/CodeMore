#! /usr/bin/env python3
"""
R = (A * Rn-1 + C) % M
"""

class PRNG():
    def __init__(self, seed):
        self.a =  2**32
        self.c = 1
        self.m = 22695477
        self.seed = seed

    def generator(self, status=0):
        if status:
            self.r = (self.a * status + self.c) % self.m
        else:
            self.r = (self.a * self.seed + self.c) % self.m
        return self.r

    def next(self):
        return self.generator(self.r)

if __name__ == "__main__":
    prng = PRNG(1013904223)
    print(prng.generator())

    counts = 0
    while True:
        print(prng.next())
        if counts >= 10:
            break