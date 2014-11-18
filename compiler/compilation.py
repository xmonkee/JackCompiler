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

    def is_next_token(self, k_list = None, v_list = None):
        """if next token is k:v, checks whether
        k is k_list and v is in v_list"""
        tag = self.tokens[self.pos].keys()[0]
        val = self.tokens[self.pos].values()[0]
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
        return tag,val

class CompilationEngine:
    """The recursive compilation engine for Jack"""

    def __init__(self, tokens):
        """Initialize token stream"""
        self.tr = TokenReader(tokens)

    def compile_class(self):
        sub = []
        self.update_kw(sub,'class')
        self.update_ident(sub) #classname
        self.update_sym(sub, '{')
        while self.tr.is_next_token(['keyword'], ['static', 'field']):
            sub.append(self.compile_classVarDec()) 
        while self.tr.is_next_token(['keyword'], ['constructor', 'function', 'method']):
            sub.append(self.compile_subroutineDec())
        self.update_sym(sub, "}")
        return {'class':sub}

    def compile_classVarDec(self):
        sub = []
        self.update_kw(sub, 'static', 'field') 
        self.update(sub, ['keyword', 'identifier']) #type
        self.update_ident(sub) #varname
        while self.tr.is_next_token(['symbol'], [',']):
            self.update_sym(sub, ',') 
            self.update_ident(sub) #varname
        self.update_sym(sub,';')
        return {'classVarDec':sub}
        
    def compile_subroutineDec(self):
        sub = []
        self.update_kw(sub, 'constructor', 'function', 'method')
        self.update(sub, ['keyword', 'identifier']) #type
        self.update_ident(sub)
        self.update_sym(sub,'(')
        if self.tr.is_next_token(['keyword','identifier']): #at least 1 param
            sub.append(self.compile_parameterList())
        self.update_sym(sub,')')
        sub.append(self.compile_subroutineBody())
        return {'subroutineDec': sub}
    
    def compile_parameterList(self):
        sub = []
        self.update(sub, ['keyword', 'identifier']) #type
        self.update_ident(sub)
        while self.tr.is_next_token(['symbol'], [',']): #more params
            self.update_sym(sub, ',') 
            self.update(sub, ['keyword', 'identifier']) #type
            self.update_ident(sub) #varname
        return {'parameterList' : sub}

    def compile_subroutineBody(self):
        sub = []
        self.update_sym(sub, '{')
        while self.tr.is_next_token(['keyword'],['var']):
            sub.append(self.compile_varDec())
        sub.append(self.compile_statements())
        self.update_sym(sub, '}')
        return {'subroutineBody': sub}

    def compile_varDec(self):
        sub = []
        self.update_kw(sub,'var')
        self.update(sub, ['keyword', 'identifier']) #type
        self.update_ident(sub) #varname
        while self.tr.is_next_token(['symbol'], [',']):
            self.update_sym(sub, ',') 
            self.update(sub, ['keyword', 'identifier']) #type
            self.update_ident(sub) #varname
        return {'varDec':sub}


    def compile_statements(self):
        sub = []
        while self.tr.is_next_token(['keyword'], ['let', 'if', 'while', 'do', 'return']):
            if self.tr.is_next_token(['keyword'],['let']):
                sub.append(self.compile_letStatement())
            elif self.tr.is_next_token(['keyword'],['if']):
                sub.append(self.compile_ifStatement())
            elif self.tr.is_next_token(['keyword'],['while']):
                sub.append(self.compile_whileStatement())
            elif self.tr.is_next_token(['keyword'],['do']):
                sub.append(self.compile_doStatement())
            elif self.tr.is_next_token(['keyword'],['return']):
                sub.append(self.compile_returnStatement())
        return {'statements':sub}
    
    def compile_letStatement(self):
        sub = []
        self.update_kw(sub,'let')
        self.update_ident(sub) #varname
        if self.tr.is_next_token(['symbol'],['[']): #array access
            self.update_sym(sub,'[')
            sub.append(self.compile_expression())
            self.update_sym(sub,']')
        self.update_sym(sub,'=')
        sub.append(self.compile_expression())
        self.update_sym(sub,';')
        return {'letStatement':sub}

    def compile_expression(self):
        sub = []
        sub.append(self.compile_term())
        while self.tr.is_next_token(['symbol'],list("+-*/&|<>=")):
            self.update_sym(sub)
            self.append(self.compile_term())
        print sub
        return {'expression':sub}

    def compile_term(self):
        sub = []
        if self.tr.is_next_token(['integerConstant']):
            self.update_int(sub)
        elif self.tr.is_next_token(['stringConstant']):
            self.update_str(sub)
        elif self.tr.is_next_token(['keyword']):
            self.update_kw(sub,'true','false','null','this')
        elif self.tr.is_next_token(['identifier']): 
            self.update_ident(sub)
            if self.tr.is_next_token(['symbol'],['[']): #varname [ expression ]
                self.update_sym(sub,'[')
                sub.append(self.compile_expression())
                self.update_sym(sub,']')
            elif self.tr.is_next_token(['symbol'],['(']): #Subroutine call
                self.update_sym(sub,'(')
                sub.append(self.compile_expressionList())
                self.update_sym(sub,')')
            elif self.tr.is_next_token(['symbol'],['.']): #classname|varname.method call
                self.update_sym(sub,'.')
                self.update_ident(sub) #method/function name
                self.update_sym(sub,'(')
                sub.append(self.compile_expressionList())
                self.update_sym(sub,')')
        elif self.tr.is_next_token(['symbol'],['(']): #sub expression
            self.update_sym(sub,'(')
            sub.append(self.compile_expression())
            self.update_sym(sub,')')
        elif self.tr_is_next_token(['symbol'], ['-','~']): #unaryOp
            self.update_sym(sub, '-', '~')
            sub.append(self.compile_term())
        return {'term':sub}

    def compile_expressionList(self):
        sub = []
        sub.append(self.compile_expression())
        while self.tr.is_next_token(['symbol'],[',']):
            self.update_sym(sub, ',')
            sub.append(self.compile_expression())
        return {'expressionList':sub}

    def update(self, sub, klist=None, vlist=None):
        """Helper functions to get and parse next token pair
        and update sub with that value"""
        tag,val = self.tr.get(klist,vlist)
        sub.append({tag:val})
    def update_kw(self, sub, *vlist):
        self.update(sub,['keyword'],None if vlist is () else vlist)
    def update_ident(self, sub, *vlist):
        self.update(sub,['identifier'],None if vlist is () else vlist)
    def update_sym(self, sub, *vlist):
        self.update(sub,['symbol'], None if vlist is () else vlist)
    def update_int(self, sub, *vlist):
        self.update(sub,['integerConstant'], None if vlist is () else vlist)
    def update_str(self, sub, *vlist):
        self.update(sub,['stringConstant'], None if vlist is () else vlist)
        
        



        



