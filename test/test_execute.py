import pytest
from scheme import translate
from scheme.executor import execute
from scheme.model import Variable, Symbol, Vector, ProcedureCall, Context, Lambda, SingleParameter, FixedParameters, ParametersWithLast
from util import default_context, procedure, quote, t_

@pytest.mark.parametrize("text,expected", [
    ("(quote a)", Symbol('a')),
    ("(quote #(a b c))", Vector((Symbol('a'), Symbol('b'), Symbol('c')))),
    ("(quote (+ 1 2))", (Symbol('+'), 1, 2)),
    ("'a", Symbol('a')),
    ("'#(a b c)",  Vector((Symbol('a'), Symbol('b'), Symbol('c')))),
    ("'()", ()),
    ("'(+ 1 2)", (Symbol('+'), 1, 2)),
    ("'(quote a)", (Symbol('quote'), Symbol('a'))),
    ("''a", (Symbol('a'))),
    ("'\"abc\"", "abc"),
    ("\"abc\"", "abc"),
    ("'145932", 145932),
    ("'#t", True),
    ("#t", True),
])
def test_literal(text, expected):
    print(execute(translate(text), default_context()))
    assert expected == execute(translate(text), default_context())

def test_variable():
    ast = translate('a')
    context = default_context()
    result = execute(ast, context.bind(Variable("a"), 1))
    assert 1 == result

@pytest.mark.parametrize("text,expected", [
    ('(let ((x 1)) (lambda (y) (+ x y)))', Lambda(FixedParameters(t_(Variable('y'))),
                                                  t_(ProcedureCall(Variable('+'), t_(Variable('x'), Variable('y')))),
                                                  default_context({Variable('x'):1}))),
    ('(lambda (x y) x)', Lambda(FixedParameters(t_(Variable('x'), Variable('y'))),
                                t_(Variable('x')),
                                default_context())),
    ('(lambda (x . y) x)', Lambda(ParametersWithLast(t_(Variable('x')), Variable('y')),
                                  t_(Variable('x')),
                                  default_context())),
])
def test_lambda(text, expected):
    context = default_context()
    assert expected == execute(translate(text), default_context())

@pytest.mark.parametrize("text,expected", [
    ("((lambda x (+ x 1)) 2)", 3),
    ("((lambda (x) (+ x x)) 4)", 8),
    ("(define reverse-subtract (lambda (x y) (- y x))) (reverse-subtract 7 10) ", 3),
    ("(define add4 (let ((x 4)) (lambda (y) (+ x y)))) (add4 6)  ", 10),
])
def test_procedure(text, expected):
    context = default_context()
    print(execute(translate(text), context))
    print(context)
    assert expected == execute(translate(text), default_context())

def test_definition():
    ast = translate("""
    (define add1 (lambda x (+ x 1)))
    (add1 3)""")
    result = execute(ast, default_context())
    assert 4 == result

@pytest.mark.parametrize("text,expected", [
    ("(if (> 3 2) 'yes 'no)", Symbol('yes')),
])
def test_conditional(text, expected):
    ast = translate(text)
    assert expected == execute(ast, default_context())

@pytest.mark.parametrize("text,expected", [
    ("(define x 1) (set! x 2) (+ x 1)", 3),
])
def test_set_(text, expected):
    ast = translate(text)
    assert expected == execute(ast, default_context())


@pytest.mark.parametrize("text,expected", [
    ( "(cond ((= 2 1) 'a))", ()),
    ( "(cond ((= 1 1) 'a))", Symbol("a")),
    ( "(cond ((= 2 1) 'a) (else 'b))", Symbol("b")),
    ( "(cond ((+ 2 1) => (lambda x (+ 4 x))))", 7)
])
def test_cond(text, expected):
    ast = translate(text)
    assert expected == execute(ast, default_context())

@pytest.mark.parametrize("text,expected", [
    ("(and (= 2 2) (> 2 1))", True),
    ("(and (= 2 2) (< 2 1))", False),
    ("(and 1 2 'c '(f g))", (Symbol("f"), Symbol("g"))),
    ("(and)", True),
    ("(or (= 2 2) (> 2 1))", True),
    ("(or (= 2 2) (< 2 1))", True),
    ("(or #f #f #f)", False),
    #("(or (memq 'b '(a b c)) (/ 3 0))", (Symbol("b"), Symbol("c"))),     
])
def test_and_or(text, expected):
    ast = translate(text)
    assert expected == execute(ast, default_context())
