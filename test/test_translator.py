import pytest
from scheme import translate
from scheme.model import Identifier, ProcedureCall, Symbol, Lambda, Variable, Character, Vector, Definition

@pytest.mark.parametrize("text,expected", [
    ('16', 16),
    ('"hello world"', "hello world"),
    (r'#\\t', Character("t")),
    (r'#t', True),
    (r'#f', False),
    ("'17", 17),
    #("`17", 17),
    #(",17", 17),
    #(",@17", 17),
    #("#(17)", 17),
    ("(quote 17)", 17),
    (r"'(1 2 3)", (1, 2, 3)),
    (r"""'#(0 (2 2 2 2) "Anna")""", Vector((0, (2, 2, 2, 2), "Anna"))),
    (r"'()", ()),
    (r"'nil", Symbol("nil")),
])
def test_literal(text, expected):
    result = translate(text).commands[0]
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ('a', Variable('a')),
])
def test_procedure_call(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ('(a)', ProcedureCall(Identifier('a'), ())),
    ('(+ 1 2)', ProcedureCall(Identifier('+'), (1,2))),
])
def test_procedure_call(text, expected):
    result = translate(text).commands[0]
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ('(lambda () 0)', Lambda((), (0,))),
    ('(lambda x (+ x 1))', Lambda((Variable('x'),), (ProcedureCall(Variable('+'), (Variable('x'), 1)),))),
    ('(lambda x ((lambda y 1) x))', Lambda( (Variable('x'),), (ProcedureCall( Lambda( (Variable('y'),), (1,)), (Variable('x'),)),))),
])
def test_lambda(text, expected):
    result = translate(text).commands[0]
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ("(define x 1)", Definition(Variable("x"), 1)),
    ("(define x (lambda x (+ 1 x)))", Definition( Variable("x"), Lambda( (Variable('x'),), (ProcedureCall(Variable('+'), (1, Variable('x'))),)))),
])
def test_definition(text, expected):
    assert expected == translate(text).commands[0]