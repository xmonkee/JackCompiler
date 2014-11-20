#Author: Mayank Mandava
#Jack Compiler

from tokenreader import TokenReader
from datafuncs import NamedStruct, And, Or, Maybe, Star, Atom

def compile_class(tokens):
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

subroutineCall = Or(
        And(subroutineName, 
            symbol('('), expressionList, symbol(')')),
        And(Or(className, varName), 
            symbol('.'), 
            subroutineName, 
            symbol('('), expressionList, symbol(')')))

def term(*params):
    return NamedStruct('term',
            Or( integerConstant, stringConstant, keywordConstant,
                And(varName, symbol('['), expression, symbol(']')), 
                subroutineCall,
                And(symbol('('), expression, symbol(')')), 
                And(unaryOp, term), varName))(*params)
        

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

