import pytest
from scheme import execute

@pytest.mark.parametrize("text,expected", [
    ("(eqv? 'a 'a)", True),
    ("(eqv? 'a 'b)", False),
    ("(eqv? 2 2)", True),
    ("(eqv? '() '())", True),
    ("(eqv? 100000000 100000000)", True),
    #("(eqv? (cons 1 2) (cons 1 2))", False),
    ("(eqv? #f 'nil)", False),
    ("(let ((p (lambda (x) x))) (eqv? p p))", False),
    ("(let ((p (lambda (x) x))) (eqv? p p))", False),
])
def test_eqv(text, expected):
    assert expected == execute(text)

@pytest.mark.parametrize("text, expected", [
    ("(eq? 'a 'a)", True),
    ("(eq? (list 'a) (list 'a))", False),
    ("(eq? '() '())", True),
    ("(eq? car car)", True),
    ("(let ((n (+ 2 3))) (let ((x '(a))) (eq? x x))", True),
    ("(let ((x '#())) (eq? x x))", True),
    ("(let ((p (lambda (x) x))) (eq? p p))", True),
])
def test_eq(text, expected):
    assert expected == execute(text)

@pytest.mark.parametrize("text, expected", [
    ("(equal? 'a 'a)", True),
    ("(equal? '(a) '(a))", True),
    ("(equal? '(a (b) c) '(a (b) c))", True),
    ('(equal? "abc" "abc")', True),
    ("(equal? 2 2)", True),
    ("(equal? (make-vector 5 'a) (make-vector 5 'a))", True),
])
def test_equal(text, expected):
    assert expected == execute(text)

def test_sum():
    assert 5 == execute('(+ 2 3)')

@pytest.mark.parametrize("text, expected", [
    ('(= 2 2)', True),
    ('(= 0)', True),
])
def test_number_eq(text, expected):
    assert expected == execute(text)