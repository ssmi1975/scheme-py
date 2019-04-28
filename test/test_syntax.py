import pytest
import scheme.parser as parser

@pytest.mark.parametrize("identifier", ["lambda", "q", "list->vector", "soup", "+", "V17a",
        "<=?", "a34kTMNs" "the-word-recursion-has-many-meanings"])
def test_identifier(identifier):
    parser.parser(parser.identifier).parse(identifier)
    
def test_comment():
    text = """;;; The FACT procedure computes the factorial
;;; of a non-negative integer.
(define fact
  (lambda (n)
    (if (= n 0)
        1        ;Base case: return 1
        (* n (fact (- n 1)))
    )
  )
)
    """
    parser.parser().parse(text)
    
