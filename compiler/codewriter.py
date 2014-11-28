#Author: Mayank Mandava
#JackCompiler: CodeWriter

#This module writes the actual vm code
#functions correspond to vm commands

from symboltable import Variable

class CodeWriter(object):
   def __init__(self):
      self.vmcode = ""

   def function(self, state):
      outs = "function {cname}.{fname} {localc}"
      outs = outs.format(
            cname=state['classname'],
            fname=state['fname'],
            localc=state['sym_tbl'].count('local'))
      self.vmcode += outs+"\n"
      if state['fkind'] == 'constructor':
         self.push('constant', state['sym_tbl'].count('field'))
         self.call('Memory', 'alloc', 1)
         self.pop('pointer', 0)
      if state['fkind'] == 'method':
         self.push('argument', 0)
         self.pop('pointer', 0)
      return

   def call(self, classname, fname, argc):
      self.vmcode += "call %s.%s %s\n" %(classname, fname, argc)
      return

   def pop(self, segment, cnt):
      self.vmcode += ("pop %s %s\n" % (segment, cnt))
      
   def push(self, segment, cnt):
      self.vmcode += ("push %s %s\n" % (segment, cnt))

   def push_var(self, var):
      name, kind, type_, num = var
      if name == 'this':
         self.vmcode += "push pointer 0\n"
      else:
         seg = 'this' if kind=='field' else kind
         self.vmcode += "push %s %s\n" % (seg, num)
               
   def pop_var(self, var):
      name, kind, type_, num = var
      seg = 'this' if kind=='field' else kind
      self.vmcode += "pop %s %s\n" % (seg, num)
   
   def push_this(self):
      self.vmcode += "push pointer 0\n"
      return

   def pop_this(self):
      self.vmcode += "pop pointer 0\n"
      return

   def raw(self, r):
      self.vmcode += (r + "\n")

   def label(self, l, cnt=""):
      self.vmcode += "label %s%s\n" % (l, cnt)
   def if_goto(self, l, cnt=""):
      self.vmcode += "if-goto %s%s\n" % (l, cnt)
   def goto(self, l, cnt=""):
      self.vmcode += "goto %s%s\n" % (l, cnt)

   def string(self, s):
      self.push('constant', len(s))
      self.call("String", "new", 1)
      for letter in s:
         self.push('constant', ord(letter))
         self.call("String", "appendChar", 2)
      return


   def get_code(self):
      return self.vmcode
