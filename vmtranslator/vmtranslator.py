import parser
import mapping

def translate(inlines):
    outlines = []
    forest = parser.parse(inlines)
    for tree in forest:
        fn, args, sourceline = tree
        outlines.append("//"+sourceline)
        outlines.append(mapping.__dict__['M_'+fn](*args))
    return outlines

        



