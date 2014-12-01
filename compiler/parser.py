#Author: Mayank Mandava
#Jack Compiler

#################################################################
# The following is a straightforward translation of the Jack
# grammar into parsing function. 

# Instead of writing each function manually, we rely on the 
# meta-structures in datafuncs.py to translate the grammar
# This lets us define our grammar declaratively instead of 
# procedurally and the resulting code is much shorter

# Each element here is a function that 
# can take the token reader object and parse it recursively.
# The elements are arranged bottom up to avoid calling functions
# that haven't been defined yet. In case recursion or mutual 
# recursion is unavoidable, the elemnet is defined explicitly
# as a function with def because that python allows mutual
# recursion in def structures. 

###############################################################

from tokenreader import TokenReader
from datafuncs import NamedStruct, And, Or, Maybe, Star, Atom

def parse_class(tokens):
    tr = TokenReader(tokens)
    return class_(tr)

def symbol(sym):
    return Atom('symbol', [sym])

def keyword(kw):
    return Atom('keyword', [kw])



keywordConstant = Atom('keyword', ['true','false','null','this'])
integerConstant = Atom('integerConstant')
stringConstant = Atom('stringConstant')
className = subroutineName = varName = Atom('identifier')

unaryOp = Atom('symbol', ['-','~'])
op = Atom('symbol', list("+-*/|=")+['&lt;','&gt;','&amp;'])

def expression(*params):
    return NamedStruct('expression', And(term, Star(And(op, term))))(*params)

expressionList = NamedStruct('expressionList', 
        Maybe(
            And(expression, 
                Star(And(symbol(','), expression)))))

subroutineCall = NamedStruct('subroutineCall', Or(
        And(subroutineName, 
            symbol('('), expressionList, symbol(')')),
        And(Or(className, varName), 
            symbol('.'), 
            subroutineName, 
            symbol('('), expressionList, symbol(')'))))

def term(*params):
    return NamedStruct('term',
            Or( integerConstant, stringConstant, keywordConstant,
                NamedStruct('arrayAccess', And(varName, symbol('['), expression, symbol(']'))), 
                subroutineCall,
                NamedStruct('bracketExp', And(symbol('('), expression, symbol(')'))), 
                NamedStruct('unaryOpTerm', And(unaryOp, term)), 
                varName))(*params)
        

returnStatement = NamedStruct('returnStatement', 
        And( keyword('return'), 
            Maybe(expression), symbol(';')))

doStatement = NamedStruct('doStatement', 
        And(keyword('do'), 
            subroutineCall, 
            symbol(';')))

def whileStatement(*params):
    return NamedStruct('whileStatement', 
            And(keyword('while'), symbol('('), 
                expression, symbol(')'), 
                symbol('{'), statements, symbol('}'))
            )(*params)

def ifStatement(*params):
    return NamedStruct('ifStatement', 
            And(keyword('if'), symbol('('), expression, symbol(')'), 
            symbol('{'), statements, symbol('}'), 
            Maybe(And(keyword('else'), symbol('{'), statements, symbol('}'))))
            )(*params)

letStatement = NamedStruct('letStatement', 
        And(keyword('let'), varName, 
        Maybe(And(symbol('['), expression, symbol(']'))), 
        symbol('='), expression, symbol(';')))

statement = Or(letStatement, ifStatement, 
        whileStatement, doStatement, 
        returnStatement)

def statements(*params):
    return NamedStruct('statements', 
            Star(statement))(*params)

type_ = Or(keyword('int'), 
        keyword('char'), 
        keyword('boolean'), 
        className)

varDec = NamedStruct('varDec', 
        And(keyword('var'), type_, varName, 
            Star(And(symbol(','), varName)), 
            symbol(';')))

subroutineBody = NamedStruct('subroutineBody', 
        And(symbol('{'), 
            Star(varDec), statements, 
            symbol('}')))

parameterList = NamedStruct('parameterList', 
        Maybe(
            And(type_, varName, 
                Star(And(symbol(','), type_, varName)))))

subroutineDec = NamedStruct('subroutineDec', 
        And(Or(keyword('constructor'), keyword('function'), keyword('method')), 
            Or(keyword('void'), type_), 
            subroutineName, 
            symbol('('), parameterList, symbol(')'), 
            subroutineBody))

classVarDec = NamedStruct('classVarDec', 
        And(Or(keyword('static'), keyword('field')), type_, varName, 
            Star(And(symbol(','), varName)),
            symbol(';')))

def class_(*params):
    return NamedStruct('class', 
            And(keyword('class'), className, 
                symbol('{'),
                Star(classVarDec), 
                Star(subroutineDec),
                symbol('}')))(*params)

