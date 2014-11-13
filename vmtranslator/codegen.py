#Author: Mayank Mandava
#The code generation module. 
#The functions are stored as M_name where name is the same as the parsed command. 
#This allows us to introspect this module and map source commands directly to functions
#The functions are called by the assembler with the current state(keeping track of the current class and function name etc) and the arguments for that particular command. 

from functools import wraps

location = {'constant':0, 'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT', 'pointer':3, 'temp':5, 'static':16}

def breaklines(f):
    """Decorator to return one command per line"""
    @wraps(f)
    def breakf(*args, **kwargs):
        out = f(*args, **kwargs)
        return '\n'.join(out.split())
    return breakf

@breaklines
def init():
   """Initialize and Call Sys.init"""
   out = "@256 D=A @SP M=D "
   return out  + M_call({'count':0}, 'Sys.init', 0)

@breaklines
def M_push(state, seg, val):
    if seg == 'constant':
        return """@{val} D=A @SP M=M+1 A=M-1 M=D""".format(val=val)
    elif seg == 'static':
        return """@{cname}.{val} D=M @SP M=M+1 A=M-1 M=D""".format(
              cname=state['classname'], val=val)
    else:
        out = """@{val} D=A @{location} A=D+{AorM} D=M @SP M=M+1 A=M-1 M=D"""
        AorM = 'A' if seg in {'pointer', 'temp'} else 'M'
        return out.format(val=val, location=location[seg], AorM=AorM)

@breaklines
def M_pop(state, seg, val):
    if seg == 'static':
       return "@SP AM=M-1 D=M @{cname}.{val} M=D".format(
              cname=state['classname'], val=val)
    else:
       out = """@{val} D=A @{location} D=D+{AorM} @R13 M=D @SP AM=M-1 D=M @R13 A=M M=D""" 
       AorM = 'A' if seg in {'pointer', 'temp'} else 'M'
       return out.format(val=val, location=location[seg], AorM=AorM)

@breaklines
def M_add(state):
    return """@SP AM=M-1 D=M A=A-1 M=D+M"""

@breaklines
def M_sub(state):
    return """@SP AM=M-1 D=M A=A-1 M=M-D"""

@breaklines
def M_neg(state):
    return "@SP A=M-1 M=-M"

@breaklines
def M_not(state):
    return "@SP A=M-1 M=!M"

@breaklines
def M_and(state):
    return """@SP AM=M-1 D=M A=A-1 M=D&M"""

@breaklines
def M_or(state):
    return """@SP AM=M-1 D=M A=A-1 M=D|M"""

def M_eq(state):
    return M_eqltgt('eq', state['count'])
def M_lt(state):
    return M_eqltgt('lt', state['count'])
def M_gt(state):
    return M_eqltgt('gt', state['count'])

@breaklines
def M_eqltgt(cond, count):
    """Common function for eq lt and gt"""
    out = """@SP AM=M-1 D=M  A=A-1 D=M-D @TRUE{count} D;{jcond}
    @SP A=M-1 M=0 @CONTINUE{count} 0;JMP
    (TRUE{count}) @SP A=M-1 M=-1 (CONTINUE{count})"""
    #count is a running counter to avoid duplication of labels
    jcond = {'lt':'JLT', 'gt':'JGT', 'eq':'JEQ'}[cond]
    return out.format(jcond=jcond, count=count)

@breaklines
def M_label(state, label):
   return "({}${})".format(state['funcname'], label)

@breaklines
def M_goto(state, label):
    return "@{}${} 0;JMP".format(state['funcname'], label)

@breaklines
def M_if_goto(state, label):
    return """@SP AM=M-1 D=M @{f}${l} D;JNE""".format(f=state['funcname'], l=label)

@breaklines
def M_function(state, fname, lcount):
   #lcount is number of local variables
   out = "("+fname+") " #function label
   out += "@SP A=M " #point to SP
   out += "M=0 A=A+1 "*int(lcount) #push lcount 0's
   out += "D=A @SP M=D" #update SP
   return out

@breaklines
def M_call(state, fname, argc):
   # Push return address
   # Push LCL
   # Push ARG
   # Push THIS
   # Push That
   # ARG = SP-n-5
   # LCL = SP
   # (return address)

   return """
   @RETPOINT{count} D=A
   @SP M=M+1 A=M-1 M=D
   @LCL D=M
   @SP M=M+1 A=M-1 M=D
   @ARG D=M
   @SP M=M+1 A=M-1 M=D
   @THIS D=M
   @SP M=M+1 A=M-1 M=D
   @THAT D=M
   @SP M=M+1 A=M-1 M=D
   @SP D=M @{argc} D=D-A @5 D=D-A
   @ARG M=D
   @SP D=M @LCL M=D
   @{fname} 0;JMP 
   (RETPOINT{count})
   """.format(count=state['count'], argc=argc, fname=fname) 

@breaklines
def M_return(state):
   # FRAME = LCL
   # RET = *(FRAME-5)
   # *ARG = pop()
   # SP = ARG+1
   # THAT = *(FRAME-1)
   # THIS = *(FRAME-2)
   # ARG = *(FRAME-3)
   # LCL = *(FRAME-4)
   # goto RET
   return (
   "@LCL D=M @R13 M=D " + #R13 stores LCL
   "@5 A=D-A D=M @R14 M=D " + #R14 stores return address
   "@SP A=M-1 D=M @ARG A=M M=D " + #return value stored in ARG0
   "@ARG D=M+1 @SP M=D " + #set SP to ARG+1
   "@R13 AM=M-1 D=M @THAT M=D " + #restore THAT
   "@R13 AM=M-1 D=M @THIS M=D " + #restore THIS
   "@R13 AM=M-1 D=M @ARG M=D " + #restore ARG
   "@R13 AM=M-1 D=M @LCL M=D " + #restore LCL
   "@R14 A=M 0;JMP ") #Jump to return address




   

