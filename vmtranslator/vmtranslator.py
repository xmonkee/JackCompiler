#Author: Mayank Mandava
#This provides the glue between the parser and the translator functions
#We optinally include the sources lines in our asm output

import parser
import mapping

def translate(inlines, isdir, keepsource):
    outlines = []
    if isdir: 
        outlines.append(mapping.init())
    forest = parser.parse(inlines)
    for tree in forest:
        command, state, args = tree
        if keepsource: outlines.append("//"+state['line'])
        try:
            out = mapping.__dict__['M_'+command](state, *args)
            outlines.append(mapping.__dict__['M_'+command](state, *args))
            #The mapping is done by the function names
        except KeyError as e:
            raise Exception("Cannot parse: "+state['line'])
    return outlines
