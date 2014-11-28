#Author: Mayank Mandava
#JackCompiler: AST Reader

class AstReader():
   def __init__(self, ast):
      self.ast = ast
      self.pos = 0

   def get(self):
      "return the first value in ast"
      if isinstance(self.ast, list):
         if self.pos < len(self.ast):
            return self.ast[self.pos]
         else:
            return None
      else:
         return self.ast
         

   def get_key(self):
      "return the key of the first ast"
      if self.get() is None:
         return None
      return self.get().keys()[0]

   def get_val(self):
      "return the key of the first ast"
      if self.get() is None:
         return None
      return self.get().values()[0]

   def next(self):
      "return first value and move head by 1"
      toret = self.get()
      self.pos += 1
      return toret

   def next_key(self):
      "return next key and move one step"
      return self.next().keys()[0]

   def next_val(self):
      "return next value and move one step"
      return self.next().values()[0]

   def next_sec(self):
      "return next section as ast object"
      return AstReader(self.next_val())

