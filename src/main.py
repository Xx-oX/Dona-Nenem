#!/usr/bin/env python

import sys
from parse import parse
from parse import gen

file_in = ""
file_out = ""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Wrong argument!!!")
        
    file_in = sys.argv[1]
    if file_in.count(".arxml") < 1:
        sys.exit("Wrong input file type!!")
    file_out = file_in[:file_in.index(".arxml")] + ".oil"

    AST = parse(file_in)
    gen(AST, file_out)
