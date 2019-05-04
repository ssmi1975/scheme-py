import pytest
from scheme import translate
from scheme.model import *
from util import quote, procedure

@pytest.mark.parametrize("text,expected", [
    ('16', 16),
    ('"hello world"', "hello world"),
    (r'#\\t', Character("t")),
    (r'#t', True),
    (r'#f', False),
    ("'17", quote(17)),
    #(",17", 17),
    #(",@17", 17),
    #("#(17)", Vector((17,))),
    ("(quote 17)", quote(17) ),
    ( r"'(1 2 3)", quote((1, 2, 3)) ),
    ( r"""'#(0 (2 2 2 2) "Anna")""", quote(Vector((0, (2, 2, 2, 2), "Anna"))) ),
    ( r"'()", quote(()) ),
    ( r"'nil", quote(Symbol("nil")) ),
    ( r"''a", quote(quote(Symbol("a"))) ),
    ( r"(quote (+ 1 2))", quote((Symbol("+"), 1, 2)) ),
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
    ('(a)', ProcedureCall(Variable('a'), ())),
    ('(+ 1 2)', ProcedureCall(Variable('+'), (1,2))),
])
def test_procedure_call(text, expected):
    result = translate(text).commands[0]
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ('(lambda () 0)', Lambda(FixedParameters(()), (0,), Context())),
    ('(lambda x (+ x 1))', Lambda(SingleParameter(Variable('x')),
                                  (ProcedureCall(Variable('+'), (Variable('x'), 1)),),
                                  Context())),
    ('(lambda x ((lambda y 1) x))', Lambda(SingleParameter(Variable('x')),
                                           (ProcedureCall( Lambda(SingleParameter(Variable('y')),
                                                                  (1,),
                                                                  Context()),
                                                           (Variable('x'),)),),
                                           Context())),
    ('(lambda (x y) x)', Lambda(FixedParameters((Variable('x'), Variable('y'))),
                                (Variable('x'),),
                                Context())),
    ('(lambda (x . y) x)', Lambda(ParametersWithLast((Variable('x'),), Variable('y')),
                                  (Variable('x'),),
                                  Context())),
    ('(lambda (x y . z) x)', Lambda(ParametersWithLast((Variable('x'),Variable('y')), Variable('z')),
                                  (Variable('x'),),
                                  Context())),
])
def test_lambda(text, expected):
    result = translate(text).commands[0]
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ("(define x 1)", Definition(Variable("x"), 1)),
    ("(define x (lambda x (+ 1 x)))", Definition( Variable("x"), Lambda( SingleParameter(Variable('x')),
                                                                         (ProcedureCall(Variable('+'), (1, Variable('x'))),),
                                                                         Context()))),
])
def test_definition(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ("(if (= 3 2) 'yes 'no)", Conditional(ProcedureCall(Variable('='), (3, 2)), ProcedureCall(Variable('quote'), (Symbol('yes'),)), ProcedureCall(Variable('quote'), (Symbol('no'),)))),
    ("((if #f - +) 3 4)", ProcedureCall(Conditional(False, Variable('-'), Variable('+')), (3, 4))),
])
def test_conditional(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ("(let ((x 3)) x)", Let(((Variable('x'), 3),), (Variable('x'),))),
])
def test_let(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ("(set! x 1)", Set_(Variable("x"), 1)),
])
def test_set_(text, expected):
    assert expected == translate(text).commands[0]