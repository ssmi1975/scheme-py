from arpeggio import visit_parse_tree, PTNodeVisitor
from .parser import parse
from .model import (Identifier, ProcedureCall, Symbol, Variable, Lambda, Character, Vector, Definition, Program,
 Conditional, Quotation, Let, SingleParameter, FixedParameters, ParametersWithLast, Context)
import copy

import pprint

def to_tuple(value):
    if isinstance(value, list):
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
        return to_tuple(children)

    def visit_vector(self, node, children):
        return Vector(to_tuple(children))

    def visit_quotation(self, node, children):
        return Quotation(children[0])

    #def visit_identifier(self, node, children):
        #return Identifier(node.value)

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
        return Let(to_tuple(children[0]), children[1])

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


VISITOR = SchemeASTVisitor(debug=False)
def translate(tree):
    return visit_parse_tree(tree, VISITOR)

