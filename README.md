#Jack Stack
Author: Mayank Mandava
Email: mayankmandava@gmail.com

##JackCompiler.py
   This is the top level command line interface to the compiler. 
   Usage: ./JackCompiler.py source
   Source can be either individual .jack file or a directory containing jack files
   Each .jack file is compiled to a .xml file

###Modules within compiler folder:

   compiler.py: This calls the tokenizer, and passes the tokens to the compiler
      Then it takes the nested datastructure returned by the compiler and converts it to xml and returns it back to the calling program

   tokenizer.py: Parses the text and converts it to a token-stream based on the grammar

   tokenreader.py: This is used by the compiler to read and consume the tokenstream. It has pretty extensive sytax checking capabilities and program should find any syntax errors

   datafuncs.py: This contains the grammatical meta-structures that are used to generate the compiler functions for the different grammatical elements. It's a sort of a DSL used to write the parsing functions 

   compilation.py: The main compilation module. This is a straighforward translation of the grammatical structure into functions that rely on the meta-structures in datafuncs

   compilation_old.py: This was the first version of the compiler I wrote. It has the exact same functionality as compilation.py but does't use the DSL. All the functions are written manually and tends to be long-ish. To use this version in stead of the current one, modify compiler.py and change "from compilation import compile_class" to "from compilation_old.py import compile_class"


###Requirements:
 Python 2.7. The program assumes a unix-like environment with python 2.7 installed and available via /usr/bin/env. If it’s not, please run with python interpreter explicitly. Example: /path/to/python.exe JackTranslator.py source

###Folders:
 compiler/ - contains the tokenizer and compiler modules
 tools/ - utility tools including command line parsing and white space removal

#Other programs:

##VMTranslator.py
 This program translates a .vm file or a direcotry containing several .vm files into a hack .asm file
 Usage: ./VMTranslator.py source [keep-source]
 source is either a single .vm file or a directory containing .vm files
 If source is a direcory, the output is saved in source.asm next to the directory and the program is initialized by setting SP and calling Sys.init
 If the source is a file, SP is not set and Sys.init is not called. 
 The optional keep-source flag, if supplied, will preserve the source vm commands as comments in the asm code

###Files:
   VMTranslator.py: Command line program to translate .vm files 
   vmtranslator/codegen.py : code generation
   vmtranslator/parser.py : parser
   vmtranslator/vmtranslator.py : the actual translator, calls parser and maps commands to the code generator

###Requirements:
 Python 2.7. The program assumes a unix-like environment with python 2.7 installed and available via /usr/bin/env. If it’s not, please run with python interpreter explicitly. Example: /path/to/python.exe VMTranslator.py source

##Assembler.py
 This program is used to compile Hack assembly code to Hack machine language
 Usage: ./Assembler.py filename.asm

##White_space_killah.py
 This program is used to remove whitespaces from source files
 Usage: ./White_space_killah.py infile.in [no-comments]

###Folders:
 vmtranslator/ - the code for the translator and parser
 assembler/ - the code for the assembler, parser, symbol table and translator
 tools/ - utility tools including command line parsing and white space removal
 tests/ - test files

