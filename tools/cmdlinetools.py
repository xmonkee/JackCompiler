#Author: Mayank Mandava

def parse_args(comp_args, flags=[], msg="Incorrect Usage"):
    """Parses command line arguments. comp_args is a list of compulsary arguments, 
    flags is a list of optional boolean flags, msg is what is displayed if the 
    commandline has less than the compulsary number of arguments"""
    import sys
    outdict = {}
    if len(sys.argv) < 1+len(comp_args):
        print msg
        sys.exit(0)
    i = 0
    for arg in comp_args:
        i += 1
        outdict[arg] = sys.argv[i]
    for flag in flags:
        outdict[flag] = flag in sys.argv[i+1:]
    return outdict      

def change_extension(filename, outext):
    """Change file.xyz to file.outext"""
    k = filename.rfind('.')
    if k < 0:
        return filename + "." + outext
    else:
        return filename[:k]+"."+outext
