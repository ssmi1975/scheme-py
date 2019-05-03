import pytest
from scheme import translate
from scheme.executor import execute
from scheme.model import Variable, Symbol, Vector, Quotation, ProcedureCall, Context, Lambda, SingleParameter, FixedParameters, ParametersWithLast
from scheme.stdproc import BINDINGS

def default_context(extra_bindings={}):
    c = Context(bindings=BINDINGS)
    for k,v in extra_bindings.items():
        c = c.bind(k, v)
    return c

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
    print(execute(translate(text), default_context()))
    assert expected == execute(translate(text), default_context())

def test_variable():
    ast = translate('a')
    context = default_context()
    result = execute(ast, context.bind(Variable("a"), 1))
    assert 1 == result

@pytest.mark.parametrize("text,expected", [
    ('(let ((x 1)) (lambda (y) (+ x y)))', Lambda(FixedParameters((Variable('y'),)),
                                                  (ProcedureCall(Variable('+'), (Variable('x'), Variable('y'))),),
                                                  default_context({Variable('x'):1}))),
    ('(lambda (x y) x)', Lambda(FixedParameters((Variable('x'), Variable('y'))),
                                (Variable('x'),),
                                default_context())),
    ('(lambda (x . y) x)', Lambda(ParametersWithLast((Variable('x'),), Variable('y')),
                                  (Variable('x'),),
                                  default_context())),
])
def test_lambda(text, expected):
    context = default_context()
    assert expected == execute(translate(text), default_context())

@pytest.mark.parametrize("text,expected", [
    ("((lambda x (+ x 1)) 2)", 3),
    ("((lambda (x) (+ x x)) 4)", 8),
    ("(define reverse-subtract (lambda (x y) (- y x))) (reverse-subtract 7 10) ", 3),
    #("(define add4 (let ((x 4)) (lambda (y) (+ x y)))) (add4 6)  ", 10),
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
