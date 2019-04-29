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