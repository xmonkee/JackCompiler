#Author: Mayank Mandava
#Jackcompiler: Code generator

from symboltable import SymbolTable
from astreader import AstReader

def codegen(ast):
   """Top level code generator function"""
   ast = AstReader(ast)
   vmcode = CodeGenerator().codegen(ast)
   return vmcode

class CodeGenerator():
   def __init__(self):
      self.vmcode = ""

   def codegen(self, ast):
      """Entry point into codeGenerator.Starts the recursive compilation and 
      returns the final result to calling function"""
      self.class_({},ast.next_sec())
      return self.vmcode

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
      fkind = ast.next_val() #constructor, function, method
      frettype = ast.next_val() #retune type
      fname = ast.next_val() #function name
      state= state.copy() #we keep a local frame for each function
      statelocal['sym_tbl'] = SymbolTable(state['sym_tbl']) 
      statelocal['fkind'] = fkind
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
         self.varDec(self, state, ast)
      return


   def varDec(self, state, ast):
      return

      
      


      
   
