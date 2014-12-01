#Author: Mayank Mandava
#Jackcompiler

#This file contains the grammatical meta-structures of the jack grammar
#specification. The most basic is the Atom: a single element that is not 
#composed of any other elements and is directly to be found in the token stream
#The other structures are: 
#   And: element1 element2 ...
#   Or: element1 | element2 ...
#   NamedStructure: those elements that produce a nested structure like class, expression etc
#   Maybe: (element)?
#   Star: element*

# Each function produces a parsing function with 2 capabilities, 
# apply and check.
# Apply is the default behaviour. It will absorb tokens from the 
# token stream and compile them and return the result
# Check will only verify that the particular structure is actually 
# present on the token stream. Most structures only check the 
# first token but the And structure can look ahead to any number 
# of elements, depending on the setting LD. 
# Here, we have set LD to 2 since the grammar is LL(1) at most. 
# Both APPLY and CHECK will eventually trickly down to Atom. All APPLY 
# calls are guarded with an assert so all syntax is checked automatically
# the ld setting is also trickled down, so if there is a nested AND and LD is s# set to 2, the next 3 tokens get checked.


APPLY = 1
CHECK = 2

LD = 2 #Lookup distance


def Atom(tag, vals=None):
    def call(tr, func = APPLY, ld=0):
        if func == APPLY:
            try:
                assert call(tr, CHECK)
            except:
                print tag, vals
                print tr.current()
                raise
            return tr.get()
        else:
            return tr.is_next_token([tag], vals, ld)
    return call

def And(*parts):
    def call(tr, func = APPLY, ld=0):
        if func == APPLY:
            sub = []
            for part in parts:
                to_append = part(tr)
                if isinstance(to_append, list):
                    sub += to_append
                else:
                    sub.append(to_append)
            return sub
        else:
            check = True
            for i in range(LD):
                check = check and parts[i](tr, CHECK, i+ld)
            return check
    return call

def Or(*options):
    def call(tr, func=APPLY, ld=0):
        if func==APPLY:
            for option in options:
                if option(tr, CHECK):
                    return option(tr)
        else:
            for option in options:
                if option(tr,CHECK, ld):
                    return True
            return False
    return call

def NamedStruct(name, part):
    def call(tr, func=APPLY, ld=0):
        if func == APPLY:
            ret = part(tr)
            if isinstance(ret, list):
                return {name:ret}
            else:
                return {name:[ret]}
        else:
            return part(tr, CHECK, ld)
    return call

def Maybe(part):
    def call(tr, func=APPLY, ld=0):
        if func==APPLY:
            if part(tr,CHECK):
                return part(tr)
            else:
                return []
        else:
            return True
    return call

def Star(part):
    def call(tr, func=APPLY, ld=0):
        if func==APPLY:
            sub = []
            while part(tr, CHECK):
                to_append = part(tr)
                if isinstance(to_append, list):
                    sub += to_append
                else:
                    sub.append(to_append)
            return sub
        else:
            return True
    return call


