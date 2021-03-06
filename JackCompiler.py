#!/usr/bin/env python
#Author: Mayank Mandava
#Jack Compiler
#Usage: ./JackCompiler.py source

#This program is the command line interface to the JackCompiler. It parses the user input and passes the file text to the compile module found in the compilersubdirectory. That's where all the interesting bits are

import tools.cmdlinetools as cmd
from compiler.compiler import compile
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
            outvm = compile(intext)
            outvname = cmd.change_extension(fname,"vm")
            with open(outvname,'w') as ofile:
               ofile.write(outvm)
    except Exception as e: #catch any parsing errors
        print e
        raise
        sys.exit(0)

if __name__=='__main__':
    main()
