import pytest
import scheme.parser as parser

@pytest.mark.parametrize("identifier", ["lambda", "q", "list->vector", "soup", "+", "V17a",
        "<=?", "a34kTMNs" "the-word-recursion-has-many-meanings"])
def test_identifier(identifier):
    parser.parser(parser.identifier).parse(identifier)
    
    
