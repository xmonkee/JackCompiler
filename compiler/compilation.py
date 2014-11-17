#Author: Mayank Mandava
#Jack Compiler

class TokenReader:
    """Class used to keep track of tokens and our position in it"""
    def __init__(self, tokens):
        self.tokens = tokens['tokens']
        self.length = len(self.tokens)
        self.pos = 0

    def has_more_tokens(self):
        print self.pos, self.length, self.pos < self.length
        return self.pos < self.length

    def is_next_token(self, k_list, v_list):
        """if next token is k:v, checks whether
        k is k_list and v is in v_list"""
        tag = self.tokens[self.pos].keys()[0]
        val = self.tokens[self.pos].values()[0]
        return (tag in k_list) and (val in v_list)


    def get(self):
        """Return the next tag and value from token list"""
        if not self.has_more_tokens():
            raise IndexError
        tag = self.tokens[self.pos].keys()[0]
        val = self.tokens[self.pos].values()[0]
        self.pos += 1
        return tag,val

class CompilationEngine:
    """The recursive compilation engine for Jack"""

    def __init__(self, tokens):
        """Initialize token stream"""
        self.tr = TokenReader(tokens)

    def compile_class(self):
        t_kw,kw = self.tr.get()
        t_ident,ident = self.tr.get()
        t_sym, sym = self.tr.get()
        sub =  [{t_kw:kw}, #class keyword
               {t_ident:ident}, #class name 
               {t_sym:sym}] #open braces
        while self.tr.is_next_token(['keyword'], ['static', 'field']):
            sub.append(self.compile_classVarDec())
        while self.tr.is_next_token(['keyword'], ['constructor', 'function', 'method']):
            sub.append(self.compile_subroutineDec())
        t_sym, sym = self.tr.get() #close braces
        sub.append({t_sym:sym}) 
        return {'class':sub}

    def compile_classVarDec(self):
        t_kw,kw = self.tr.get() #static or field
        t_ident, ident = self.tr.get()  #type
        t_var, var = self.tr.get() #varName
        sub = [{t_kw:kw}, {t_ident:ident}, {t_var:var}]
        while self.tr.is_next_token(['symbol'], [',']):
            t_sym,sym = self.tr.get() #comma
            t_var, var = self.tr.get() #varName
            sub.append({t_sym:sym})
            sub.append({t_var:var})
        t_sym,sym = self.tr.get() #comma
        sub.append({t_sym:sym}) #semicolon
        return {'classVarDec':sub}

        



