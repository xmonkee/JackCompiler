#Author: Mayank Mandava
#The main compiler function
#Calls the tokenizer, parser and code generator

from tokenizer import tokenize
from compilation import CompilationEngine

def compile(intext):
    tokens = tokenize(intext)
    print py2xml(tokens)
    compeng = CompilationEngine(tokens)
    return py2xml(compeng.compile_class())
    

def py2xml(data):
    """Converts nested python lists and dictionaries to XML"""
    if isinstance(data, list):
        out = ""
        for item in data:
            out += py2xml(item)
        return out
    if isinstance(data, dict):
        out = ""
        for k in data.keys():
            out += "<%s>"%k 
            if not isinstance(data[k],str): 
                out+= "\n"
            out += py2xml(data[k]) + "</%s>\n"%k 
        return out
    return data
