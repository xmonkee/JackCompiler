#Author: Mayank Mandava
#This is the parser for the vm language.


def split_line(line):
    """Return a tuple containing the command(push, add) etc and the arguments as the second componenet (local 0, or nothing in case of add etc"""
    words = line.split()
    return words[0], words[1:]

def parse(lines):
    forest = [] #output tree
    count = 0 #keeps counter of comparison command labels
    for line in lines:
        command, args = split_line(line)
        if command in ['eq','lt','gt']:  #common function and counter
            args = [command, count]
            command = 'eqltgt'
            count += 1
        forest.append([command,args, line]) 
        #we save the line for commenting output code
    return forest
