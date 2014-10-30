#Author: Mayank Mandava


def make_symbol_table(forest):
    tbl = { 
            'SP'    : 0,
            'LCL'   : 1,
            'ARG'   : 2,
            'THIS'  : 3,
            'THAT'  : 4,
            'SCREEN':16384,
            'KBD'   :24576
            }
    for i in range(16):
        #R0 to R15
        tbl['R%d'%i] = i
    line = 0  #line numbers
    free = 16 #current free memory location
    for tree in forest:
        if tree[0] == 'L':
            tbl[tree[1]] = line
        else:
            line += 1
    for tree in forest:
        if tree[0] == 'A' and tree[1][0] == 'SYM':
            if not tbl.has_key(tree[1][1]):
                tbl[tree[1][1]] = free
                free += 1
    return tbl
            

