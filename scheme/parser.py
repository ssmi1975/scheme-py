from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, Not, visit_parse_tree, PTNodeVisitor, ParserPython
from arpeggio import RegExMatch as _

def comment(): return _(r';+[^\n]*')
def start(): return (program, EOF)

def syntactic_keyword(): return [expression_keyword , "else" , "=>" , "define" , "unquote" , "unquote-splicing"]
def expression_keyword(): return ["quote" , "lambda" , "if" , "set!" , "begin" , "cond" , "and" , "or" , "case"
        , "let" , "let*" , "letrec" , "do" , "delay" , "quasiquote"]
def identifier(): return [peculiar_identifier, normal_identifier]
def normal_identifier(): return _('[a-z|$%&*,:<=>?^_~][a-z0-9!$%&*,:<=>?^_~+-.@]*')
def peculiar_identifier(): return ["+" , "-" , ellipsis]
def variable(): return Not(syntactic_keyword), identifier

def literal(): return [quotation , self_valuating]
def quotation(): return [("'", datum) ,("(", "quote", datum, ")")]
def number(): return _("[0-9]+")
def boolean(): return  ["#t" , "#f"]
def character(): return r"#\\", _(r".")
def string(): return '"', _(r'[^"\\]*'), '"'

# 7.1.2 External representations
def datum(): return [simple_datum, complex_datum, quotation]
def simple_datum(): return [boolean, number, character, string, symbol]
def symbol(): return identifier
def complex_datum(): return [_list, vector]
def _list(): return  [("(", ZeroOrMore(datum), ")"), ("(", OneOrMore(datum), ".", datum, ")")] #, abbreviation]
def abbreviation(): return abbrev_prefix, datum
def abbrev_prefix(): return  ["'" , "`" , "," , ",@"]
def vector(): return  "#(", ZeroOrMore(datum), ")"

# 7.1.3
def expression(): return [variable, procedure_call, lambda_expression, conditional, literal, derived_expression]
def self_valuating(): return [boolean, number, character, string]
    
def procedure_call(): return  "(", operator, ZeroOrMore(operand), ")"
def operator(): return expression
def operand(): return expression

def lambda_expression(): return "(", "lambda", formals, body, ")"
def formals(): return [single_parameter, fixed_parameters, parameters_with_last]
def single_parameter(): return variable
def fixed_parameters(): return "(", ZeroOrMore(variable), ")"
def parameters_with_last(): return "(", OneOrMore(variable), ".", variable, ")"
def body(): return ZeroOrMore(definition), sequence
def sequence(): return OneOrMore(expression)

def conditional(): return "(", "if", expression, expression, Optional(expression), ")"
def derived_expression(): return [let, set_, cond, or_, and_]
def let(): return "(", "let", "(", ZeroOrMore(binding_spec), ")", body, ")"
def binding_spec(): return "(", variable, expression, ")"
def set_(): return "(", "set!", variable, expression, ")"
def cond(): return "(", "cond", OneOrMore([cond_clause, cond_call]), Optional(else_clause), ")"
def cond_clause(): return "(", expression, ZeroOrMore(expression), ")"
def cond_call(): return "(", expression, "=>", expression, ")"
def else_clause(): return "(", "else", OneOrMore(expression), ")"
def or_(): return "(", "or", ZeroOrMore(expression), ")"
def and_(): return "(", "and", ZeroOrMore(expression), ")"


# 7.1.5 transformers
def transformer_spec(): return "(", "syntax-rules", "(", ZeroOrMore(symbol), ")", ZeroOrMore(syntax_rule), ")"
def syntax_rule(): return "(", pattern, template, ")"
def pattern(): return [pattern_identifier,
                       ("(", ZeroOrMore(pattern), ")"),
                       pattern_with_last,
                       ("(", OneOrMore(pattern), ellipsis, ")"),
                       ("#(", ZeroOrMore(pattern), ")"),
                       ("#(", OneOrMore(pattern), ellipsis, ")"),
                       pattern_datum]
def pattern_with_last(): return ("(", OneOrMore(pattern), ".", pattern, ")")
def pattern_datum(): return [string, character, boolean, number]
def template(): return [pattern_identifier,
                        ("(", ZeroOrMore(template_element), ")"),
                        template_with_last,
                        ("#(", ZeroOrMore(template_element), ")"),
                        ("(", pattern_datum, ")")]
def template_with_last(): return ("(", OneOrMore(template_element), ".", template, ")")
def template_element(): return [template, (template, ellipsis)]
def pattern_identifier(): return Not(ellipsis), symbol
def ellipsis(): return "..."

# 7.1.6 programs and definitions
def program(): return ZeroOrMore(command_or_definition)
def command_or_definition(): return [expression,
        definition,
        syntax_definition,
        ("(", "begin", OneOrMore(command_or_definition), ")")]
def definition(): return [ ("(", "define", variable, expression, ")"),
        ("(", "define", "(", variable, def_formals, ")", body, ")"),
        ("(", "begin", ZeroOrMore(definition), ")")
    ]
def def_formals(): return [ZeroOrMore(variable), (ZeroOrMore(variable), ".", variable)]
def syntax_definition(): return "(", "define-syntax", symbol, transformer_spec, ")"

#
def parser(entry=start, debug=False):
    return ParserPython(entry, comment, ignore_case=True, debug=debug)

def parse(text, debug=False):
    return parser(debug=debug).parse(text)

if __name__ == '__main__':
    import sys
    class TreePrinter(PTNodeVisitor):
        pass
    tree = parse(sys.stdin.read())
    visit_parse_tree(tree, visitor=TreePrinter(debug=True))