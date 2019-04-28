import pytest
from scheme import translate
from scheme.translator import Identifier, ProcedureCall

@pytest.mark.parametrize("text,expected", [
    ('16', 16),
    ('"hello world"', "hello world"),
    (r'#\\t', "t"),
    (r'#t', True),
    (r'#f', False),
    ("'17", 17),
    #("`17", 17),
    #(",17", 17),
    #(",@17", 17),
    #("#(17)", 17),
    ("(quote 17)", 17),
    (r"'(1 2 3)", [1, 2, 3]),
    (r"""'#(0 (2 2 2 2) "Anna")""", [0, [2, 2, 2, 2], "Anna"])
])
def test_literal(text, expected):
    result = translate(text)
    assert expected == result

@pytest.mark.parametrize("text,expected", [
    ('(a)', ProcedureCall(Identifier('a'), ())),
    ('(+ 1 2)', ProcedureCall(Identifier('+'), [1,2])),
])
def test_procedure_call(text, expected):
    result = translate(text)
    assert expected == result
