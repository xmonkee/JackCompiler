#Author: Mayank Mandava
#JackCompiler: CodeWriter

#This module writes the actual vm code
#functions correspond to vm commands

def add_to_vmcode(origfunc):
   def newfunc(self, *args, **kwargs):
      self.vmcode += origfunc(self, *args, **kwargs) + "\n"
      return
   return newfunc

class CodeWriter(object):
   def __init__(self):
      self.vmcode = ""

   @add_to_vmcode
   def function(self, state):
      outs = "function {cname}.{fname} {localc}"
      return outs.format(
            cname=state['classname'],
            fname=state['fname'],
            localc=state['sym_tbl'].count('local'))
      
   def get_code(self):
      return self.vmcode
