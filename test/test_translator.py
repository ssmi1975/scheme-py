import pytest
from scheme import translate

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
def test_valid(text, expected):
    result = translate(text)
    assert expected == result
