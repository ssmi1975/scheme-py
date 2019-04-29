from scheme import translate
from scheme.executor import execute
from scheme.model import Variable

def test_variable():
    ast = translate('a')
    result = execute(ast, {Variable("a"): 1})
    assert 1 == result

def test_procedure():
    ast = translate("((lambda x (+ x 1)) 2)")
    result = execute(ast, {})
    assert 3 == result

def test_definition():
    ast = translate("""
    (define add1 (lambda x (+ x 1)))
    (add1 3)""")
    result = execute(ast, {})
    assert 4 == result
