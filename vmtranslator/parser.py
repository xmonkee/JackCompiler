#Author: Mayank Mandava
#This is the parser for the vm language.


def split_line(line):
    """Return a tuple containing the command(push, add) etc and the arguments as the second componenet (local 0, or nothing in case of add etc"""
    words = line.split()
    return words[0], words[1:]

def parse(lines):
    forest = [] #output tree
    state = {'funcname':"", #name of current function
            'count':1, #running count of ad-hoc labels for VM implementation
            'line' : "", #The current source line
            'classname': "" #The current class name
            } #Any state in the compiler is stored here
    for line in lines:
        command, args = split_line(line)
        if command == 'class':
           state['classname'] = args[0]
        else:
           if command == 'if-goto': command = 'if_goto'
           if command in ['eq','lt','gt', 'call']: state['count'] += 1
           if command in ['function']: state['funcname'] = args[0]
           state['line'] = line 
           forest.append([command, state.copy(), args]) 
    return forest
