#Author: Mayank Mandava
#Jackcompiler: Code generator

# This module takes the ast produced by the parser and converts it to vm code
# It employs 3 modules: 
#  symboltable: to maintain the variable symbol table
#  astreader: for easy processing of ast
#  codewriter: writes the actual vm code
# Function names correspond to sections of the grammar
# All functions take 2 variables here: state and ast
# State is threaded into each function carrying information from 
# previous functions like classname, functionnames, and the sybol table
# ast is the part of the ast relevant to each function

from symboltable import SymbolTable
from astreader import AstReader
from codewriter import CodeWriter

def codegen(ast):
   """Top level code generator function"""
   ast = AstReader(ast)
   vmcode = CodeGenerator().codegen(ast)
   return vmcode

class CodeGenerator():
   def __init__(self):
      self.codewriter = CodeWriter()

   def codegen(self, ast):
      """Entry point into codeGenerator.Starts the recursive compilation and 
      returns the final result to calling function"""
      self.class_({},ast.next_sec())
      print self.codewriter.get_code()
      return self.codewriter.get_code()

   def class_(self, state, ast):
      """Create class symbol table and pass on control to classVarDec and 
      subroutineDec.  No code geneartion here"""
      ast.next() #'class keyword'
      state['classname'] = ast.next_val()
      ast.next() #'{'
      state['sym_tbl'] = SymbolTable()
      while(ast.get_key() == 'classVarDec'):
         self.classVarDec(state, ast.next_sec())
      while(ast.get_key() == 'subroutineDec'):
         self.subroutineDec(state, ast.next_sec())
      return

   def classVarDec(self, state, ast):
      """Parse static and field and add to symbol table"""
      var_kind = ast.next_val()
      var_type = ast.next_val()
      var_name = ast.next_val()
      state['sym_tbl'].add(var_name, var_kind, var_type)
      while(ast.next_val() != ';'):
         var_name = ast.next_val()
         state['sym_tbl'].add(var_name, var_kind, var_type)
      return

   def subroutineDec(self, state, ast):
      statelocal = state.copy() #we keep a local frame for each function
      statelocal['sym_tbl'] = SymbolTable(state['sym_tbl']) 
      statelocal['fkind'] = ast.next_val() #constructor, function, method
      statelocal['fype']= ast.next_val() #return type
      statelocal['fname'] = ast.next_val() #function name
      #new symbol table with parent linkage
      ast.next() #'('
      self.parameterList(statelocal,ast.next_sec())
      ast.next() #')'
      self.subroutineBody(statelocal, ast.next_sec())
      return
   
   def parameterList(self, state, ast):
      if state['fkind']=="method": #we have to add 'self' as first argument
         state['sym_tbl'].add('this', 'arg', state['classname']) 
      if(ast.get_val() != ")"):
         var_type = ast.next_val()
         var_name = ast.next_val()
         state['sym_tbl'].add(var_name, 'arg', var_type)
         while(ast.get_val() == ','):
            ast.next()
            var_type = ast.next_val()
            var_name = ast.next_val()
            state['sym_tbl'].add(var_name, 'arg', var_type)
      return

   def subroutineBody(self, state, ast):
      ast.next() # '{'
      while(ast.get_key() == 'varDec'):
         self.varDec(state, ast.next_sec())
      self.codewriter.function(state)
      self.statements(state, ast.next_sec())
      return

   def varDec(self, state, ast):
      ast.next() #'var'
      var_type = ast.next_val()
      var_name = ast.next_val()
      state['sym_tbl'].add(var_name, 'local', var_type)
      while(ast.next_val() != ';'):
         var_name = ast.next_val()
         state['sym_tbl'].add(var_name, 'local', var_type)
      return

   def statements(self, state, ast):
      xstatements = {
            'returnStatement':self.returnStatement,
            'ifStatement':self.ifStatement,
            'letStatement':self.letStatement,
            'whileStatement':self.whileStatement,
            'doStatement':self.doStatement }
      xstatement = ast.get_key()
      while(xstatement is not None):
         xstatements[xstatment](state, ast.next_sec())
         xstatement = ast.get_key()
      return

  def doStatement(self, state, ast):
     


      
      


      
   
