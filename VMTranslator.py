#!/usr/bin/env python
#Hack VM Translator
#Author: Mayank Mandava
#Usage: ./VMTranslator.py source [keep-source]

from tools.white_space_killah import kill_white_spaces
from vmtranslator.vmtranslator import translate
import tools.cmdlinetools as cmd
import sys
import os


def main():
    msg = "Unknown command\nUsage: {} source [keep-source]".format(sys.argv[0])
    args = cmd.parse_args(['source'], ['keep-source'], msg)
    source = args['source']
    isdir = False
    if os.path.isdir(source): #source is a directory
        isdir = True
        inlines = []
        for fname in os.listdir(source):
            if fname.endswith(".vm"):
                inlines += ["class "+fname[:-3]]  #attach classnames
                with open(source+'/'+fname, 'r') as f:
                    inlines += kill_white_spaces(f.readlines(), True, False)
    elif os.path.isfile(source): #source is a file
        with open(source, 'r') as f:
            inlines = kill_white_spaces(f.readlines(), True, False)
    else:
        print "Cannot open {}".format(source)
        sys.exit(0)

    try: 
        outlines = translate(inlines, isdir, args['keep-source'])
    except Exception as e: #catch any parsing errors
        print e
        sys.exit(0)
    outname = cmd.change_extension(source,"asm")
    with open(outname,'w') as ofile:
       ofile.writelines([line+'\n' for line in outlines])


if __name__=='__main__':
    main()
