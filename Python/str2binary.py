#! coding: utf-8

import sys

if __name__=="__main__":
    origin = sys.argv[1]
    str_list = [format(ord(x), 'b') for x in origin]
    binary_chars = " ".join(str_list)
    print("[*] Source: {}".format(origin))
    print("[*] Binary: {}".format(binary_chars))
