from arpeggio import visit_parse_tree, PTNodeVisitor
from .parser import parse
from .model import *
import copy

import pprint


def _assert_type(obj, *types):
    return type(obj) in types, "expected {}, given {}".format(types, type(obj))

def _a_assert_type(obj, *types):
    try:
        assert type(obj) in types, "expected {}, given {}".format(types, type(obj))
    except AssertionError as e:
        e.__traceback__ = None
        raise e


def _assert_tuple_of_types(obj, *types):
    return all((type(o) in types for o in obj)),  "expected {}, given {}".format(types, [type(o) for o in obj])


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
    
    def visit_transformer_spec(self, node, children):
        _assert_tuple_of_types(children, Symbol, SyntaxRule)
        ids = to_tuple((s for s in children if type(s) == Symbol)),
        rules = to_tuple((s for s in children if type(s) == SyntaxRule))
        print(children)
        print(ids)
        print(rules)
        return TransformerSpec(ids, rules)

    def visit_syntax_rule(self, node, children):
        assert len(children) == 2
        a = _assert_type(children[0], Pattern); assert a[0], a[1]
        a = _assert_type(children[1], Template); assert a[0], a[1]
        return SyntaxRule(children[0], children[1])

    def visit_pattern(self, node, children):
        a = _assert_tuple_of_types(children, Pattern, PatternDatum, Symbol); assert a[0], a[1]
        if len(children) == 0:
            return Pattern()
        elif type(children[-1]) == Ellipsis:
            return Pattern(children[:-1], has_ellipsis=True)
        else:
            return Pattern(children)

    def visit_pattern_with_last(self, node, children):
        assert len(children) > 1
        a = _assert_tuple_of_types(children, Pattern, PatternDatum, Symbol); assert a[0], a[1]
        return Pattern(children, has_ellipsis=False, capture_last=True)

    def visit_pattern_datum(self, node, children):
        assert len(children) == 1
        a = _assert_type(children[0], str, int, Character, bool); assert a[0], a[1]
        return PatternDatum(children[0])

    def visit_template(self, node, children):
        a = _assert_tuple_of_types(children, Template, PatternDatum, Symbol); assert a[0], a[1]
        if len(children) == 0:
            return Template()
        if type(children[-1]) == Ellipsis:
            return Template(children[:-1], has_ellipsis=True)
        else:
            return Template(children)

    def visit_template_with_last(self, node, children):
        assert len(children) > 1
        a = _assert_tuple_of_types(children, Template, PatternDatum, Symbol); assert a[0], a[1]
        return Template(children, has_ellipsis=False, capture_last=True)

    def visit_template_element(self, node, children):
        assert len(children) < 3
        a = _assert_tuple_of_types(children, Template, PatternDatum, Symbol); assert a[0], a[1]
        if len(children) == 1:
            return Template(children[0])
        else:
            return Template(children[0], True)
    
    def visit_template_datum(self, node, children):
        assert len(children) == 1
        a = _assert_type(children[0], PatternDatum); assert a[0], a[1]
        return children[0]
    
    def visit_pattern_identifier(self, node, children):
        assert len(children) == 1
        a = _assert_type(children[0], Symbol); assert a[0], a[1]
        return children[0]

    def visit_ellipsis(self, node, children):
        assert len(children) == 1
        return Ellipsis()
    
    def visit_syntax_definition(self, node, children):
        assert len(children) == 2
        a = _assert_type(children[0], Symbol); assert a[0], a[1]
        #a = _assert_type(children[1], TransformerSpec); assert a[0], a[1]
        _a_assert_type(children[1], TransformerSpec)
        return SyntaxDefinition(children[0], children[1])

VISITOR = SchemeASTVisitor(debug=False)
def translate(tree):
    return visit_parse_tree(tree, VISITOR)


if __name__ == '__main__':
    from scheme.parser import parse
    translate(parse('(let ((x 3)) x)'))
