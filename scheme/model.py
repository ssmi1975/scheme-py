from collections import namedtuple

class Context:
    def __init__(self, bindings={}, parameters=[]):
        self.bindings = bindings
        self.parameters = parameters
    
    def bind(self, variable, value):
        new_context = self.copy()
        new_context.bindings[variable] = value
        return new_context
    
    def update_bindings(self, variable, value):
        self.bindings[variable] = value
    
    def enter(self, parameter):
        new_context = self.copy()
        new_context.parameters.append(parameter)
        return new_context
    
    def copy(self):
        return Context(self.bindings.copy(), self.parameters.copy())
    
    def __repr__(self):
        return "Context(bindings={}, parameters={})".format(self.bindings, self.parameters)
    
    def __eq__(self, other):
        return self.bindings == other.bindings and self.parameters == other.parameters


Symbol = namedtuple('Symbol', 'name')

Variable = namedtuple('Variable', 'name')

ProcedureCall = namedtuple('ProcedureCall', ('operator', 'operand'))

Lambda = namedtuple('Lambda', ('formals', 'body', 'context'))
SingleParameter = namedtuple('SingleParameter', 'name')
FixedParameters = namedtuple('FixedParameters', 'names')
ParametersWithLast = namedtuple('ParametersWithLast', ('names', 'last'))

Vector = namedtuple('Vector', 'values')

Character = namedtuple('Character', 'value')

Definition = namedtuple('Definition', ('variable', 'expression'))

Program = namedtuple('Program', ('commands'))

Conditional = namedtuple('Conditional', ("test", "consequent", "alternate"))

Quotation = namedtuple('Quotation', "datum")

Let = namedtuple('Let', ("bindings", "body"))

PyFunction = namedtuple('PyFunction', "function")
