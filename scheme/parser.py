from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, Not, visit_parse_tree, PTNodeVisitor, ParserPython
from arpeggio import RegExMatch as _

def letter(): return _(r'[a-z]')
def digit(): return _(r'[0-9]')
def start(): return (expression, EOF)
def expression(): return [variable, literal, procedure_call, derived_expression]

def syntactic_keyword(): return [expression_keyword , "else" , "=>" , "define" , "unquote" , "unquote-splicing"]
def expression_keyword(): return ["quote" , "lambda" , "if" , "set!" , "begin" , "cond" , "and" , "or" , "case"
        , "let" , "let*" , "letrec" , "do" , "delay" , "quasiquote"]
def variable(): return (Not(syntactic_keyword), identifier)
def identifier(): return [peculiar_identifier, normal_identifier]
def normal_identifier(): return _('[a-z|$%&*,:<=>?^_~][a-z0-9!$%&*,:<=>?^_~+-.@]*')
def peculiar_identifier(): return ["+" , "-" , "..."]

def literal(): return [quotation , self_valuating]
def quotation(): return [("'", datum) ,("(", "quote", datum, ")")]
def number(): return _('[0-9]+')
def boolean(): return  ["#t" , "#f"]

def datum(): return (simple_datum, complex_datum)
def simple_datum(): return (boolean, number, symbol)
def symbol(): return identifier
def complex_datum(): return (_list, vector)
def _list(): return  [("(", datum, ZeroOrMore(datum), ")"), ("(", OneOrMore(datum), ".", datum, ")"), abbreviation]
def abbreviation(): return [abbrev_prefix, datum]
def abbrev_prefix(): return  ["'" , "`" , "," , ",@"]
def vector(): return  ("#(", ZeroOrMore(datum), ")")

def self_valuating(): return [boolean , number]
    
def procedure_call(): return  ("(", operator, ZeroOrMore(operand), ")")
def operator(): return expression
def operand(): return expression

def derived_expression(): return "ab"

def parser(entry=start):
    return ParserPython(entry, ignore_case=True)

def parse(text):
    return parser().parse(text)

if __name__ == '__main__':
    import sys
    class TreePrinter(PTNodeVisitor):
        pass
    tree = parse(sys.stdin.read())
    visit_parse_tree(tree, visitor=TreePrinter(debug=True))