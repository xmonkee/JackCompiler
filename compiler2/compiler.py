#Author: Mayank Mandava
#The main compiler function
#Calls the tokenizer, parser and code generator

from tokenizer import tokenize
from compilation import compile_class

def compile(intext):
    tokens = tokenize(intext)
    print compile_class(tokens)
    return py2xml(compile_class(tokens))
    

def py2xml(data, dist=0):
    """Converts nested python lists and dictionaries to XML"""
    if isinstance(data, dict):
        out = ""
        for k in data.keys():
            out += "<%s>"%k 
            if isinstance(data[k], list):
               out += "\n"
               out += py2xml(data[k], dist+2)
               out += " "*dist + "</%s>"%k 
            else:
               out += py2xml(data[k], dist)
               out += "</%s>"%k 
        return out
    elif isinstance(data, list):
        out = ""
        for item in data:
            out += " "*dist + py2xml(item, dist) + '\n'
        return out
    else:
        return data

