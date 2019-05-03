import pytest
import scheme.parser as parser
from scheme.translator import translate
   
    
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
    
