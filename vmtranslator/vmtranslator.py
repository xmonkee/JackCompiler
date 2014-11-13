#Author: Mayank Mandava
#This provides the glue between the parser and the translator functions
#We optinally include the sources lines in our asm output

import parser
import codegen

def translate(inlines, isdir, keepsource):
    outlines = []
    if isdir: #called on a directory, we initialize and call Sys.init()
        outlines.append(codegen.init()) 
    forest = parser.parse(inlines)
    for tree in forest:
        command, state, args = tree
        if keepsource: outlines.append("//"+state['line'])
        try:
            #The mapping is done by the function names directly
            #i.e. the 'push' command maps directly to codegen.M_push
            outlines.append(codegen.__dict__['M_'+command](state, *args))
        except KeyError as e:
            raise Exception("Cannot parse: "+state['line'])
    return outlines
