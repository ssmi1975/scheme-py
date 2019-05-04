from arpeggio import visit_parse_tree, PTNodeVisitor
from .parser import parse
from .model import *
import copy

import pprint

def is_iterable(value):
    try:
        iter(value)
        return True
    except TypeError:
        return False
    
def to_tuple(value):
    if is_iterable(value) and not isinstance(value, str):
        return tuple(value)
    return (value,)


def list_to_tuple(value):
    if isinstance(value, list):
        return tuple(value)
    return value

class SchemeASTVisitor(PTNodeVisitor):
    def __init__(self, context={}, **kwargs):
        PTNodeVisitor.__init__(self, kwargs)
        self.context = {}

    def visit_number(self, node, children):
        return int(node.value)
    
    def visit_string(self, node, children):
        return str(children[0])
   
    def visit_character(self, node, children):
        return Character(children[0])

    def visit_boolean(self, node, children):
        return node.value == "#t"

    def visit_symbol(self, node, children):
        return Symbol(node.value)

    def visit_variable(self, node, children):
        return Variable(node.value)

    def visit__list(self, node, children):
        return tuple(children)

    def visit_vector(self, node, children):
        return Vector(to_tuple(children))

    def visit_quotation(self, node, children):
        datum = children[0]
        if is_iterable(datum) and len(children[0]) == 0:
            # empty list
            return ProcedureCall(Variable('quote'), ((),))
        elif type(datum) in (bool, int, str, Character, Symbol, Vector, ProcedureCall):
            # simple value
            return ProcedureCall(Variable('quote'), (datum,))
        elif type(datum) in (list, tuple):
            return ProcedureCall(Variable('quote'), (to_tuple(datum),))
        else:
            raise(Exception("unexpected value {} (type={}) passed".format(datum, type(datum))))

    def visit_procedure_call(self, node, children):
        if len(children) == 1:
            return ProcedureCall(children[0], ())
        else:
            return ProcedureCall(children[0], to_tuple(children[1:]))

    def visit_lambda_expression(self, node, children):
        return Lambda(children[0], children[1], Context())
    
    def visit_formals(self, node, children):
        return children[0]
    
    def visit_single_parameter(self, node, children):
        return SingleParameter(Variable(children[0]))

    def visit_fixed_parameters(self, node, children):
        return FixedParameters(to_tuple(children))

    def visit_definition(self, node, children):
        return Definition(children[0], children[1])

    def visit_parameters_with_last(self, node, children):
        return ParametersWithLast(to_tuple(children[:-1]), children[-1])

    def visit_let(self, node, children):
        return Let(to_tuple(children[:-1]), children[-1])

    def visit_body(self, node, children):
        return to_tuple(children)

    def visit_binding_spec(self, node, children):
        return (children[0], children[1])

    def visit_program(self, node, children):
        return Program(to_tuple(children))
    
    def visit_conditional(self, node, children):
        if len(children) == 2:
            return Conditional(children[0], children[1],())
        else:
            return Conditional(children[0], children[1], children[2])

    def visit_set_(self, node, children):
        return Set_(children[0], children[1])

    def visit_cond_clause(self, node, children):
        return CondClause(children[0], tuple(children[1:]))

    def visit_cond_call(self, node, children):
        return CondClause(children[0], tuple(children[1:]), True)

    def visit_else_clause(self, node, children):
        return CondClause(True, to_tuple(children))

    def visit_cond(self, node, children):
        return Cond(to_tuple(children))

    def visit_and_(self, node, children):
        return And(to_tuple(children))

    def visit_or_(self, node, children):
        return Or(to_tuple(children))

VISITOR = SchemeASTVisitor(debug=False)
def translate(tree):
    return visit_parse_tree(tree, VISITOR)


if __name__ == '__main__':
    from scheme.parser import parse
    translate(parse('(let ((x 3)) x)'))
