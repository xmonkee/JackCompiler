#!/usr/bin/env python
#Hack Assembler
#Author: Mayank Mandava
#Usage: $Assembler.py filename.asm

from tools.white_space_killah import kill_white_spaces
from assembler.assembler import assemble
import tools.cmdlinetools as cmd
import sys


def main():
    args = cmd.parse_args(['filename'], msg="Please supply filename")
    filename = args['filename']
    try:
        infile = open(filename,'r')
    except:
        print "Cannot open file {}".format(filename)
        sys.exit(0)

    inlines = kill_white_spaces(infile.readlines(), True)
    try: outlines = assemble(inlines)
    except Exception as e: 
        print e
        sys.exit(0)
    outname = cmd.change_extension(filename,"hack")
    outfile = open(outname, 'w')
    outfile.writelines([line+'\n' for line in outlines])
    infile.close()
    outfile.close()


if __name__=='__main__':
    main()
