from functools import wraps

location = {'constant':0, 'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT', 'pointer':3, 'temp':5, 'static':16}

def breaklines(f):
    """Decorator to return one command per line"""
    @wraps(f)
    def breakf(*args, **kwargs):
        out = f(*args, **kwargs)
        return '\n'.join(out.split())+"\n"
    return breakf


@breaklines
def M_push(seg, val):
    if seg == 'constant':
        return """@{val} D=A @SP M=M+1 A=M-1 M=D""".format(val=val)
    else:
        out = """@{val} D=A @{location} A=D+{AorM} D=M @SP M=M+1 A=M-1 M=D"""
        AorM = 'A' if seg in {'pointer', 'temp', 'static'} else 'M'
        return out.format(val=val, location=location[seg], AorM=AorM)

@breaklines
def M_pop(seg, val):
    out = """@{val} D=A @{location} D=D+{AorM} @R13 M=D @SP AM=M-1 D=M @R13 A=M M=D""" 
    AorM = 'A' if seg in {'pointer', 'temp', 'static'} else 'M'
    return out.format(val=val, location=location[seg], AorM=AorM)

@breaklines
def M_add():
    return """@SP AM=M-1 D=M A=A-1 M=D+M"""

@breaklines
def M_sub():
    return """@SP AM=M-1 D=M A=A-1 M=M-D"""

@breaklines
def M_neg():
    return "@SP A=M-1 M=-M"

@breaklines
def M_not():
    return "@SP A=M-1 M=!M"

@breaklines
def M_and():
    return """@SP AM=M-1 D=M A=A-1 M=D&M"""

@breaklines
def M_or():
    return """@SP AM=M-1 D=M A=A-1 M=D|M"""

@breaklines
def M_eqltgt(cond, count):
    """Common function for eq lt and gt"""
    out = """@SP AM=M-1 D=M  A=A-1 D=M-D @TRUE{count} D;{jcond}
    @SP A=M-1 M=0 @CONTINUE{count} 0;JMP
    (TRUE{count}) @SP A=M-1 M=-1 (CONTINUE{count})"""
    jcond = {'lt':'JLT', 'gt':'JGT', 'eq':'JEQ'}[cond]
    return out.format(jcond=jcond, count=count)

