#!/usr/bin/env python
#Author: Mayank Mandava
#Jack Compiler
#Usage: ./JackCompiler.py source

import tools.cmdlinetools as cmd
from compiler.compiler import compile
import sys
import os


def main():
    msg = "Unknown command\nUsage: {} source".format(sys.argv[0])
    args = cmd.parse_args(['source'], ['keep-source'], msg)
    source = args['source']
    isdir = False
    if os.path.isdir(source): #source is a directory
        isdir = True
        intext = ""
        for fname in os.listdir(source):
            if fname.endswith(".jack"):
                with open(source+'/'+fname, 'r') as f:
                    intext += f.read()
    elif os.path.isfile(source): #source is a file
        with open(source, 'r') as f:
            intext = f.read()
    else:
        print "Cannot open {}".format(source)
        sys.exit(0)

    try: 
        outtext = compile(intext)
    except Exception as e: #catch any parsing errors
        print e
        #sys.exit(0)
        raise
    outname = cmd.change_extension(source,"xml")
    with open(outname,'w') as ofile:
       ofile.write(outtext)


if __name__=='__main__':
    main()
