#Author: Mayank Mandava
#This provides the glue between the parser and the translator functions
#We optinally include the sources lines in our asm output

import parser
import mapping

def translate(inlines, keepsource):
    outlines = []
    forest = parser.parse(inlines)
    for tree in forest:
        fn, args, sourceline = tree
        if keepsource: outlines.append("//"+sourceline)
        try:
            outlines.append(mapping.__dict__['M_'+fn](*args))
            #The mapping is done by the function names. We don't need an external table
            #This reduces coupling between the parser and the translator
        except Exception as e:
            raise Exception("Cannot parse: "+sourceline)
    return outlines
