#!/usr/bin/env python

# Author: Mayank Mandava
# Email: mayankmandava@gmail.com
# Standalone usage: white_space_kallah.py filename.in [no-comments]

import tools.cmdlinetools as cmd
import tools.white_space_killah as wsk

def __main():
    import sys
    msg = "Unknown command\nUsage: python {} filename [no-comments]".format(sys.argv[0])
    args = cmd.parse_args(['filename'], ['no-comments'], msg)
    try:
        infile = open(args['filename'], 'r')
    except IOError:
        print "Can't open file {}".format(args['filename'])
        sys.exit(0)
    noComments = args['no-comments']
    outname = cmd.change_extension(args['filename'], 'out')
    outfile = open(outname, 'w')
    outlines = wsk.kill_white_spaces(infile.readlines(), noComments)
    outfile.writelines(map(lambda line: line+"\n", outlines));
    infile.close
    outfile.close


if __name__=="__main__":
   __main()
