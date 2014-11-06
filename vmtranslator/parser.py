def split_line(line):
    words = line.split()
    return words[0], words[1:]

def parse(lines):
    forest = [] #output tree
    count = 0 #keeps counter of comparison commands
    for line in lines:
        command, args = split_line(line)
        if command in ['eq','lt','gt']:
            args = [command, count]
            command = 'eqltgt'
            count += 1
        forest.append([command,args, line]) 
        #we save the line for commenting output code
    return forest


        
        
        


