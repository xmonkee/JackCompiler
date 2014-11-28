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
from symboltable import Variable
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
      ast.next() #'}'
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
      statelocal['cf_count'] = 0 #control flow labels
      #new symbol table with parent linkage
      if statelocal['fkind'] == 'method':
         statelocal['sym_tbl'].var_counter['argument'] += 1
      ast.next() #'('
      self.parameterList(statelocal,ast.next_sec())
      ast.next() #')'
      self.subroutineBody(statelocal, ast.next_sec())
      return
   
   def parameterList(self, state, ast):
      if(ast.get_val() is not None):
         var_type = ast.next_val()
         var_name = ast.next_val()
         state['sym_tbl'].add(var_name, 'argument', var_type)
         while(ast.get_val() == ','):
            ast.next()
            var_type = ast.next_val()
            var_name = ast.next_val()
            state['sym_tbl'].add(var_name, 'argument', var_type)
      return

   def subroutineBody(self, state, ast):
      ast.next() # '{'
      while(ast.get_key() == 'varDec'):
         self.varDec(state, ast.next_sec())
      self.codewriter.function(state)
      self.statements(state, ast.next_sec())
      ast.next() # '}'
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
         xstatements[xstatement](state, ast.next_sec())
         xstatement = ast.get_key()
      return

   def doStatement(self, state, ast):
      ast.next() #'do'
      self.subroutineCall(state,ast.next_sec())
      self.codewriter.pop('temp',  0) #throw away void return
      ast.next() #';'
      return

   def returnStatement(self, state, ast):
      ast.next() #'return'
      if ast.get_key() == 'expression':
         self.expression(state, ast.next_sec())
      else:
         self.codewriter.push('constant', 0)
      self.codewriter.raw('return')
      ast.next() #';'
      return

   def ifStatement(self, state, ast):
      cf_count = state['cf_count']
      state['cf_count'] += 1
      ast.next() # 'if'
      ast.next() # '('
      self.expression(state, ast.next_sec())
      ast.next() # ')'
      self.codewriter.if_goto('IF_TRUE',cf_count)
      self.codewriter.goto('IF_FALSE',cf_count)
      ast.next() # '{'
      self.codewriter.label('IF_TRUE', cf_count)
      self.statements(state, ast.next_sec())
      ast.next() # '}'
      if(ast.get_val() == 'else'):
         self.codewriter.goto('IF_END',cf_count)
      self.codewriter.label('IF_FALSE', cf_count)
      if(ast.get_val() == 'else'):
         ast.next() # 'else'
         ast.next() # '{'
         self.statements(state, ast.next_sec())
         ast.next() # '}'
         self.codewriter.label('IF_END', cf_count)
      return


      self.codewriter.label('IF_FALSE', cf_count)
      return

   def whileStatement(self, state, ast):
      cf_count = state['cf_count']
      state['cf_count'] += 1
      self.codewriter.label('WHILE_EXP', cf_count)
      ast.next() # 'while'
      ast.next() # '('
      self.expression(state, ast.next_sec())
      ast.next() # ')'
      self.codewriter.raw('not')
      self.codewriter.if_goto('WHILE_END',cf_count)
      ast.next() # '{'
      self.statements(state, ast.next_sec())
      ast.next() # '}'
      self.codewriter.goto('WHILE_EXP', cf_count)
      self.codewriter.label('WHILE_END', cf_count)
      return

   def letStatement(self, state, ast):
      ast.next() # 'let'
      varname = ast.next_val()
      if ast.get_val() == '[':
         ast.next() # '['
         self.expression(state, ast.next_sec())
         self.codewriter.push_var(state['sym_tbl'].lookup(varname))
         self.codewriter.raw('add')
         ast.next() # ']'
         ast.next() # '='
         self.expression(state, ast.next_sec())
         self.codewriter.pop('temp', 0)
         self.codewriter.pop('pointer', 1)
         self.codewriter.push('temp', 0)
         self.codewriter.pop('that', 0)
      else:
         ast.next() # '='
         self.expression(state, ast.next_sec())
         self.codewriter.pop_var(state['sym_tbl'].lookup(varname))
      ast.next() # ';'
      return

   def subroutineCall(self, state, ast):
      if state['sym_tbl'].lookup(ast.get_val()) is not None: #other class method call
         objname = ast.next_val()
         obj = state['sym_tbl'].lookup(objname)
         ast.next() # dot
         fname = ast.next_val()
         self.codewriter.push_var(obj) #push object as first argument
         ast.next() # '('
         argc = self.expressionList(state, ast.next_sec()) #push other arguments 
         #argc is number of "actual" arguments
         ast.next() # ')'
         self.codewriter.call(obj.type, fname, argc+1)
      else: #not other class method call 
         firstname = ast.next_val()
         if ast.get_val() == '.': #Class.function()
            classname = firstname
            ast.next()
            fname = ast.next_val() 
            ast.next() # '('
            argc = self.expressionList(state, ast.next_sec()) #push other arguments 
            #argc is number of "actual" arguments
            ast.next() # ')'
            self.codewriter.call(classname, fname, argc)
         else: #self method call
            classname = state['classname'] #own class name
            fname = firstname
            self.codewriter.push('pointer', 0) #push this as first argument
            ast.next() # '('
            argc = self.expressionList(state, ast.next_sec()) #push other arguments 
            ast.next() # ')'
            self.codewriter.call(classname, fname, argc+1)
      return

   def expressionList(self, state, ast):
      argc = 0
      if ast.get() is not None:
         self.expression(state, ast.next_sec())
         argc += 1
         while(ast.get_val() is not None):
            ast.next()
            self.expression(state, ast.next_sec())
            argc += 1
      return argc

   def expression(self, state, ast):
      ops = {
            '+': 'add',
            '-': 'sub',
            '*': 'call Math.multiply 2',
            '/': 'call Math.divide 2',
            '|': 'or',
            '&amp;' : 'and',
            '=': 'eq',
            '&lt;' : 'lt',
            '&gt;' : 'gt'
            }
      self.term(state, ast.next_sec())
      while(ast.get_val() is not None):
         op = ast.next_val()
         self.term(state, ast.next_sec())
         self.codewriter.raw(ops[op])
      return
   
   def term(self, state, ast):
      key = ast.get_key()
      if key == 'integerConstant':
         self.codewriter.push('constant', ast.next_val())
      elif key == 'stringConstant':
         self.codewriter.string(ast.next_val())
      elif key == 'keyword':
         val = ast.next_val()
         if val == 'true':
            self.codewriter.raw('push constant 0\nnot')
         elif val == 'false':
            self.codewriter.raw('push constant 0')
         elif val == 'null':
            self.codewriter.raw('push constant 0')
         elif val == 'this':
            self.codewriter.push_this()
      elif key == 'arrayAccess':
         nast = ast.next_sec()
         varname = nast.next_val()
         nast.next() # '['
         self.expression(state, nast.next_sec())
         nast.next() # ']'
         self.codewriter.push_var(state['sym_tbl'].lookup(varname))
         self.codewriter.raw('add') #base address + index
         self.codewriter.pop('pointer', 1) #store indexed address in 'that'
         self.codewriter.push('that', 0)
      elif key == 'subroutineCall':
         self.subroutineCall(state, ast.next_sec())
      elif key == 'bracketExp':
         nast = ast.next_sec()
         nast.next() #'('
         self.expression(state, nast.next_sec())
         nast.next() #')'
      elif key == 'unaryOpTerm':
         nast = ast.next_sec()
         op = nast.next_val()
         self.term(state, nast.next_sec())
         if op == '-':
            self.codewriter.raw('neg')
         if op == '~':
            self.codewriter.raw('not')
      elif key == 'identifier':
         self.codewriter.push_var(state['sym_tbl'].lookup(ast.next_val()))
 
