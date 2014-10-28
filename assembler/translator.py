# AST to Machine Language translator
# Author: Mayank Mandava
# Usage: translate(ast)


COMP_TABLE = {
      '0'  :'101010',
      '1'  :'111111',
      '-1' :'111010',
      'D'  :'001100',
      'A'  :'110000',
      '!D' :'001101',
      '!A' :'110001',
      '-D' :'001111',
      '-A' :'110011',
      'D+1':'011111',
      'A+1':'110111',
      'D-1':'001110',
      'A-1':'110010',
      'D+A':'000010',
      'D-A':'010011',
      'A-D':'000111',
      'D&A':'000000',
      'D|A':'010101'}

DEST_TABLE = {
        ''   :'000',
        'M'  :'001',
        'D'  :'010',
        'MD' :'011',
        'A'  :'100',
        'AM' :'101',
        'AD' :'110',
        'AMD':'111'}

JMP_TABLE = {
        ''   :'000',
        'JGT':'001',
        'JEQ':'010',
        'JGE':'011',
        'JLT':'100',
        'JNE':'101',
        'JLE':'110',
        'JMP':'111'}

def dec2bin(dec, len):
   #decinal to binary
   bin = ['0']*len
   for i in range(len-1, -1, -1):
      bin[i] = dec%2
      dec = dec/2
   return ''.join(map(str,bin))


def translate(forest, sym_tbl):
   outcode = []
   for tree in forest:
      if tree[0] == 'A':
         if tree[1][0] == 'SYM':
            addr = sym_tbl[tree[1][1]]
         else: addr = tree[1][1] #direct addressing
         outcode.append('0'+ dec2bin(addr, 15))
      if tree[0] == 'C':
         dest,comp,jmp = tree[1]
         a = '1' if comp[0]=='m' else '0'
         outcode.append('111' + a + 
               COMP_TABLE[comp[1]] + 
               DEST_TABLE[dest] + 
               JMP_TABLE[jmp])
   return outcode



         
