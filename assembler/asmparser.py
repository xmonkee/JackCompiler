#Parser for Hack assembly
#Author: Mayank Mandava
#Usage : parse(list of asm statements)

import sys
import string

#contains all valid symbol characters

def parse_error(statement):
    raise Exception("Syntax Error - Cannot parse\n{} at line {}".format(statement[1], statement[0]))


def is_valid_symbol(s):
    digits = string.digits
    validchars = string.ascii_letters + string.digits + "_.$:"
    return (s[0] not in string.digits and 
            s[0] in validchars 
            and all(map(lambda c: c in validchars, s[1:])))

def is_valid_dest(dest):
   return dest in ('M,D,MD,A,AM,AD,AMD'.split(',')+[''])

def is_valid_jmp(jmp):
   return jmp in ('JGT,JEQ,JGE,JLT,JNE,JLE,JMP'.split(',')+[''])

def is_valid_comp(comp):
    unary = '0,1,-1,D,A,!D,!A,-D,-A,M,!M,-M'
    DA = 'D+1,A+1,D-1,A-1,D+A,D-A,A-D,D&A,D|A'
    DM = DA.replace('A','M')
    return comp in unary.split(',') + DA.split(',') + DM.split(',')

def parse_c_inst(statement):
    """
    c_inst = [dest]=comp;[jmp]
    """
    dest = jmp = ""
    comp = statement[1]
    try: dest,comp = comp.split("=",1)
    except: pass
    try: comp,jmp = comp.split(";",1)
    except: pass
    if not  (is_valid_dest(dest) and 
            is_valid_comp(comp) and 
            is_valid_jmp(jmp)): parse_error(statement)
    if 'M' in comp: comp = ['m', comp.replace('M','A')]
    else: comp = ['a', comp]
    return [dest, comp, jmp]


def parse_a_inst(statement):
    """
    address ::= d* | n*a*
          d ::= 0|1|...|9
          n ::= a-z|A-Z|_|.|$|:
          a ::= d|n
    """
    symbol = statement[1][1:]
    if symbol.isdigit():
        #Check if it's direct addressing
        return ['DIR', int(symbol)]
    if is_valid_symbol(symbol):
        #Or symbol
        return ['SYM', symbol]
    else: parse_error(statement)


def parse_label(statement):
    """
    label ::= (symbol)
    """
    label=statement[1]
    if (label[0]=='(' and label[-1]==')' and
        is_valid_symbol(label[1:-1])):
            return label[1:-1]
    else: parse_error(statement)


def parse_statement(statement):
    """
    statement ::= a-inst | label | c-inst
       a-inst ::= @sym | @addr
        label ::= (sym)
       c-inst ::= <everything else>
    """
    if statement[1][0]=='@':
        return ['A', parse_a_inst(statement)]
    if statement[1][0]=='(':
        return ['L', parse_label(statement)]
    else:
        return ['C', parse_c_inst(statement)]


def parse(inlines):
    """parse all input lines"""
    return map(parse_statement, enumerate(inlines))

