from arpeggio import visit_parse_tree, PTNodeVisitor
from .parser import parse
import copy


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
        return [x for x in children]

    def visit_vector(self, node, children):
        return [x for x in children]


VISITOR = SchemeASTVisitor(debug=False)
def execute(tree):
    return visit_parse_tree(tree, VISITOR)

