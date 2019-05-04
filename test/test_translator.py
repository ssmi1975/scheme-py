import pytest
from scheme import translate
from scheme.model import *
from util import quote, procedure, t_

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
    ('(a)', ProcedureCall(Variable('a'), t_())),
    ('(+ 1 2)', ProcedureCall(Variable('+'), t_(1,2))),
])
def test_procedure_call(text, expected):
    result = translate(text).commands[0]
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ('(lambda () 0)', Lambda(FixedParameters(t_()), t_(0), Context())),
    ('(lambda x (+ x 1))', Lambda(SingleParameter(Variable('x')),
                                  t_(ProcedureCall(Variable('+'), t_(Variable('x'), 1))),
                                  Context())),
    ('(lambda x ((lambda y 1) x))', Lambda(SingleParameter(Variable('x')),
                                           t_(ProcedureCall( Lambda(SingleParameter(Variable('y')),
                                                                  t_(1),
                                                                  Context()),
                                                           t_(Variable('x')))),
                                           Context())),
    ('(lambda (x y) x)', Lambda(FixedParameters(t_(Variable('x'), Variable('y'))),
                                t_(Variable('x')),
                                Context())),
    ('(lambda (x . y) x)', Lambda(ParametersWithLast(t_(Variable('x')), Variable('y')),
                                  t_(Variable('x')),
                                  Context())),
    ('(lambda (x y . z) x)', Lambda(ParametersWithLast(t_(Variable('x'),Variable('y')), Variable('z')),
                                  t_(Variable('x')),
                                  Context())),
])
def test_lambda(text, expected):
    result = translate(text).commands[0]
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ("(define x 1)", Definition(Variable("x"), 1)),
    ("(define x (lambda x (+ 1 x)))", Definition( Variable("x"), Lambda( SingleParameter(Variable('x')),
                                                                         t_(ProcedureCall(Variable('+'), (1, Variable('x')))),
                                                                         Context()))),
])
def test_definition(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ("(if (= 3 2) 'yes 'no)", Conditional(ProcedureCall(Variable('='), t_(3, 2)), ProcedureCall(Variable('quote'), t_(Symbol('yes'),)), ProcedureCall(Variable('quote'), t_(Symbol('no'))))),
    ("((if #f - +) 3 4)", ProcedureCall(Conditional(False, Variable('-'), Variable('+')), t_(3, 4))),
])
def test_conditional(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ("(let ((x 3)) x)", Let(t_(t_(Variable('x'), 3)), t_(Variable('x')))),
])
def test_let(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ("(set! x 1)", Set_(Variable("x"), 1)),
])
def test_set_(text, expected):
    assert expected == translate(text).commands[0]

@pytest.mark.parametrize("text,expected", [
    ( "(cond ((= 2 1) 'a))", Cond(t_(CondClause(procedure('=', 2, 1), t_(procedure('quote', Symbol("a")))))) ),
    ( "(cond ((= 2 1) 'a) (else 'b))", Cond(t_(CondClause(procedure('=', 2, 1), t_(procedure('quote', Symbol("a")))),
                                             CondClause(True, t_(procedure('quote', Symbol("b")))))) ),
    ( "(cond ((= 2 1) => atom?))", Cond(t_(CondClause(procedure('=', 2, 1), t_(Variable("atom?")), True))) ),
])
def test_cond(text, expected):
    assert expected == translate(text).commands[0]