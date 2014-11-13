Author: Mayank Mandava
Email: mayankmandava@gmail.com

VMTranslator.py
 This program translates a .vm file or a direcotry containing several .vm files into a hack .asm file
 Usage: ./VMTranslator.py source [keep-source]
 source is either a single .vm file or a directory containing .vm files
 If source is a direcory, the output is saved in source.asm next to the directory and the program is initialized by setting SP and calling Sys.init
 If the source is a file, SP is not set and Sys.init is not called. 
 The optional keep-source flag, if supplied, will preserve the source vm commands as comments in the asm code

Files:
   VMTranslator.py: Command line program to translate .vm files 
   vmtranslator/codegen.py : code generation
   vmtranslator/parser.py : parser
   vmtranslator/vmtranslator.py : the actual translator, calls parser and maps commands to the code generator

Requirements:
 Python 2.7. The program assumes a unix-like environment with python 2.7 installed and available via /usr/bin/env. If it’s not, please run with python interpreter explicitly. Example: /path/to/python.exe VMTranslator.py source

Other programs:

Assembler.py
 This program is used to compile Hack assembly code to Hack machine language
 Usage: ./Assembler.py filename.asm

White_space_killah.py
 This program is used to remove whitespaces from source files
 Usage: ./White_space_killah.py infile.in [no-comments]

Folders:
 vmtranslator/ - the code for the translator and parser
 assembler/ - the code for the assembler, parser, symbol table and translator
 tools/ - utility tools including command line parsing and white space removal
 tests/ - test files
