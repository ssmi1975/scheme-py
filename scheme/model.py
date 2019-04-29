from collections import namedtuple

Identifier = namedtuple('Identifier', 'name')

Symbol = namedtuple('Symbol', 'name')

Variable = namedtuple('Variable', 'name')

ProcedureCall = namedtuple('ProcedureCall', ('operator', 'operand'))

Lambda = namedtuple('Lambda', ('formals', 'body'))

StandardProcedure = namedtuple('StandardProcedure', 'name')

Vector = namedtuple('Vector', 'values')

Character = namedtuple('Character', 'value')

Definition = namedtuple('Definition', ('variable', 'expression'))

Program = namedtuple('Program', ('commands'))
