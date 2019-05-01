import pytest
from scheme import translate
from scheme.executor import execute
from scheme.model import Variable, Symbol, Vector, Quotation, ProcedureCall, Context

@pytest.mark.parametrize("text,expected", [
    ("(quote a)", Symbol('a')),
    ("(quote #(a b c))", Vector((Symbol('a'), Symbol('b'), Symbol('c')))),
    ("(quote (+ 1 2))", (Symbol('+'), 1, 2)),
    ("'a", Symbol('a')),
    ("'#(a b c)",  Vector((Symbol('a'), Symbol('b'), Symbol('c')))),
    ("'()", ()),
    ("'(+ 1 2)", (Symbol('+'), 1, 2)),
    ("'(quote a)", (Symbol('quote'), Symbol('a'))),
    ("''a", Quotation(Symbol('a'))),
    ("'\"abc\"", "abc"),
    ("\"abc\"", "abc"),
    ("'145932", 145932),
    ("'#t", True),
    ("#t", True),
])
def test_literal(text, expected):
    print(execute(translate(text), Context()))
    assert expected == execute(translate(text), Context())

def test_variable():
    ast = translate('a')
    result = execute(ast, Context(bindings={Variable("a"): 1}))
    assert 1 == result

@pytest.mark.parametrize("text,expected", [
    ("((lambda x (+ x 1)) 2)", 3),
    ("((lambda (x) (+ x x)) 4)", 8),
    ("(define reverse-subtract (lambda (x y) (- y x))) (reverse-subtract 7 10) ", 3),
    #("(define add4 (let ((x 4)) (lambda (y) (+ x y)))) (add4 6)  ", 10),
])
def test_procedure(text, expected):
    context = Context()
    print(execute(translate(text), context))
    print(context)
    assert expected == execute(translate(text), Context())

def test_definition():
    ast = translate("""
    (define add1 (lambda x (+ x 1)))
    (add1 3)""")
    result = execute(ast, Context())
    assert 4 == result

@pytest.mark.parametrize("text,expected", [
    ("(if (> 3 2) 'yes 'no)", Symbol('yes')),
])
def test_conditional(text, expected):
    ast = translate(text)
    assert expected == execute(ast, Context())
