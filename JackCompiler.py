#!/usr/bin/env python
#Author: Mayank Mandava
#Jack Compiler
#Usage: ./JackCompiler.py source

import tools.cmdlinetools as cmd
from compiler2.compiler import compile
import sys
import os


def main():
    msg = "Unknown command\nUsage: {} source".format(sys.argv[0])
    args = cmd.parse_args(['source'], ['keep-source'], msg)
    source = args['source']
    if os.path.isdir(source): #source is a directory
        files = []
        for fname in os.listdir(source):
            if fname.endswith(".jack"):
                files.append(os.path.normpath(source+'/'+fname))
    elif os.path.isfile(source): #source is a file
        files = [source]
    else:
        print "Cannot open {}".format(source)
        sys.exit(0)

    try: 
        for fname in files:
            with open(fname, 'r') as f:
                intext = f.read()
            outtext = compile(intext)
            outname = cmd.change_extension(fname,"xml")
            with open(outname,'w') as ofile:
               ofile.write(outtext)
    except Exception as e: #catch any parsing errors
        print e
        raise
        sys.exit(0)

if __name__=='__main__':
    main()
