#!/usr/bin/env python3
"""
辗转相除法,又名欧几里得算法
求解最大公约数(greatest common divisor)
a b
c = a if a < b else b // get the small one
d = a - b // get the value
"""

import sys
import argparse
sys.setrecursionlimit(1000)


def gcd(a, b):
    print(a, b)
    if a == b:
        print("gcd is {}".format(a))
        sys.exit(-1)
    else:
        c = a if a < b else b
        print("min c {}".format(c))
        d = abs(a - b)
        print("distance d {}".format(d))
        gcd(c, d)
        print(c, d)

def help():
    parse = argparse.ArgumentParser(description="greatest common divisor")
    parse.add_argument("m", type=int, help="random integer")
    parse.add_argument("n", type=int, help="random integer")
    args = parse.parse_args()
    return args

if __name__ == "__main__":
    args = help()
    gcd(args.m, args.n)
