from arpeggio import visit_parse_tree, PTNodeVisitor
from .parser import parse
import copy
import collections

Identifier = collections.namedtuple('Identifier', ('name'))

ProcedureCall = collections.namedtuple('ProcedureCall', ('operator', 'operand'))


class SchemeASTVisitor(PTNodeVisitor):
    def __init__(self, context={}, **kwargs):
        PTNodeVisitor.__init__(self, kwargs)
        self.context = {}

    def visit_number(self, node, children):
        return int(node.value)
    
    def visit_string(self, node, children):
        return str(children[0])
   
    def visit_character(self, node, children):
        return str(children[0])

    def visit_boolean(self, node, children):
        return node.value == "#t"

    def visit__list(self, node, children):
        return list(children)

    def visit_vector(self, node, children):
        return list(children)

    def visit_identifier(self, node, children):
        return Identifier(node.value)

    def visit_procedure_call(self, node, children):
        if len(children) == 1:
            return ProcedureCall(children[0], ())
        else:
            return ProcedureCall(children[0], children[1:])

    def visit_program(self, node, children):
        return Program()

VISITOR = SchemeASTVisitor(debug=False)
def translate(tree):
    return visit_parse_tree(tree, VISITOR)

