#!/usr/bin/env python
#Hack Assembler
#Author: Mayank Mandava
#Usage:
#  assemble(list of asm statements)


from asmparser import parse
from translator import translate
from symbol_table import make_symbol_table

def assemble(inlines):
    forest = parse(inlines)
    sym_tbl = make_symbol_table(forest)
    return translate(forest, sym_tbl)
