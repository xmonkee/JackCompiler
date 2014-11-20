#Author: Mayank Mandava
#Jack Compiler

class TokenReader:
    """Class used to keep track of tokens and our position in it"""
    def __init__(self, tokens):
        self.tokens = tokens['tokens']
        self.length = len(self.tokens)
        self.pos = 0

    def has_more_tokens(self):
        return self.pos < self.length

    def is_next_token(self, k_list = None, v_list = None, ld=0):
        """if next token is k:v, checks whether
        k is k_list and v is in v_list"""
        if self.pos+ld >= self.length:
            return False
        tag = self.tokens[self.pos+ld].keys()[0]
        val = self.tokens[self.pos+ld].values()[0]
        isCompliant = True
        if k_list is not None:
            isCompliant = isCompliant and (tag in k_list)
        if v_list is not None:
            isCompliant = isCompliant and (val in v_list)
        return isCompliant


    def get(self, klist = None, vlist = None):
        """Return the next tag and value from token list
        By passig klist and vlist, we can optionally check
        for syntax errors"""
        assert self.has_more_tokens()
        tag = self.tokens[self.pos].keys()[0]
        val = self.tokens[self.pos].values()[0]
        if klist is not None: 
            assert tag in klist 
            #checking we have the correct token
        if vlist is not None: 
            assert val in vlist 
            #checking we have the correct token
        self.pos += 1
        return self.tokens[self.pos-1]

    def current(self):
        print self.tokens[max(0, self.pos-5):self.pos]
        print
        print self.tokens[self.pos: min(self.length, self.pos+5)]

