# Author: Mayank Mandava
# Main tokenizer code
# Returns a stream of language atoms

import re #The regular expressions package

#Lexical Elements:

LE = [  #Lexical elements and their regular expressions
        ('stringConstant' , re.compile(r'"(.*?)"')),
        ('keyword', re.compile(r'\b(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)\b')),
        ('symbol', re.compile(r'([{}()\[\].,;+\-*/&|<>=~])')),
        ('integerConstant' , re.compile(r'(\d+)\b')),
        ('identifier' , re.compile(r'([a-zA-Z_]\w*)'))
     ]

REPLACE = {'<':'&lt;','>':'&gt;','"':'&quot;', '&':'&amp;'}

def tokenize(text):
    text = remove_comments(text)
    pos = 0 #keep track of where we are
    out = []
    while pos < len(text):
        space = re.match('\s+',text[pos:]) #remove leading spaces
        if(space):
            pos += space.end()
        for tag, pattern in LE: 
            #check in order: Strings, keywords, symbols, integers,identifiers
            match = re.match(pattern, text[pos:])
            if(match):
                matched = match.groups()[0]
                if matched in REPLACE:
                    matched = REPLACE[matched]
                out.append({tag:matched})
                pos += match.end()
                break
    return {'tokens':out} #for the opening and closing tags

def remove_comments(text):
    text = re.sub(r'//.*?$', '', text, flags=re.M)
    text = re.sub(r'/\*.*?\*/', '',text, flags=re.S)
    return text



