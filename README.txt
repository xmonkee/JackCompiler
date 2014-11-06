Author: Mayank Mandava
Email: mayankmandava@gmail.com

Assembler.py
 This program is used to compile Hack assembly code to Hack machine language

Usage:
 ./Assembler.py filename.asm

Requirements:
 Python 2.7. The program assumes a unix-like environment with python 2.7 installed and available via /usr/bin/env. If it’s not, please run with python interpreter explicitly. Example: /path/to/python.exe Assembler.py filename.asm 

Folders:
 assembler/ - the code for the assembler, parser, symbol table and translator
 tools/ - utility tools including command line parsing and white space removal
 tests/ - test ASM files
