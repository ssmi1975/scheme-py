from collections import namedtuple

class Context:
    def __init__(self, bindings={}, parameters=[]):
        self.bindings = bindings
        self.parameters = parameters
    
    def bind(self, variable, value):
        new_context = Context(self.bindings.copy(), self.parameters.copy())
        new_context.bindings[variable] = value
        return new_context
    
    def update_bindings(self, variable, value):
        self.bindings[variable] = value
    
    def enter(self, parameter):
        self.parameters.append(parameter)

    def exit(self):
        self.parameter.pop()
    
    def __repr__(self):
        return "Context(bindings={}, parameters={})".format(self.bindings, self.parameters)


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

Conditional = namedtuple('Conditional', ("test", "consequent", "alternate"))

Quotation = namedtuple('Quotation', "datum")

Let = namedtuple('Let', ("bindings", "body"))
