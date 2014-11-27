#Author: Mayank Mandava
#Jackcompiler: Code generator

from collections import namedtuple
from collections import Counter

Variable = namedtuple('Variable', 'name kind type num')

class SymbolTable():
   """Variable symbol table"""
   
   def __init__(self, parent=None):
      self.symtbl = {}
      #Dictionary of variables
      self.var_counter = Counter() 
      #Counter for each kind of variable
      self.parent = parent
      #for lookup in parent scope

   def add(self, name, kind, type_):
      self.symtbl[name] = Variable(name, kind, type_, self.var_counter[kind])
      self.var_counter[kind] += 1
   
   def lookup(self, name):
      if self.symtbl.has_key(name):
         return self.symtbl[name]
      if self.parent.lookup(name) is not None:
         return self.parent.lookup(name)
      return None

   def show(self):
      print self.symtbl
      if self.parent is not None:
         self.parent.show()
      return

   def count(self, var_kind):
      return self.var_counter[var_kind]
