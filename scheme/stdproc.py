from .model import Identifier, Symbol, Variable, Vector, Lambda, PyFunction, Context
import collections

def eqv(left, right):
    for t in (Symbol, Variable, int, StandardProcedure):
        if isinstance(left, t) and isinstance(right, t):
            return left == right
    if left == () and right == ():
        return True
    return left is right

def equal(left, right):
    return left == right

def number(value):
    return type(value) == int

def number_eq(*values):
    return all((values[0] == v for v in values))

def _assert_all_int(args):
    if not all((isinstance(arg, int) for arg in args)):
        raise(Exception("non-number value(s) are passed: {}".format(args)))

def plus(*args):
    _assert_all_int(args)
    return sum(args)

def minus(*args):
    _assert_all_int(args)
    if len(args) == 1:
        return -1 * args[0]
    if len(args) == 2:
        return args[0] - args[1]
    else:
        return args[0] - sum(args[1:])

def _list(*args):
    return tuple(args)

def _assert_pair(arg):
    if not type(arg) == tuple:
        raise(Exception("expecting pair, but got {}; value {} ".format(type(arg), arg)))

def _assert_non_empty_pair(arg):
    _assert_pair(arg)
    if len(arg) == 0:
        raise(Exception("expecting non-empty list, but an empty list"))

def _assert_int(arg):
    if not type(arg) == int:
        raise(Exception("expecting int, but got {}; value {} ".format(type(arg), arg)))

def car(args):
    _assert_non_empty_pair(args)
    return tuple(args[0])

def cdr(args):
    _assert_pair(args)
    _assert_non_empty_pair(args)
    return tuple(args[1:])

def is_atom(arg):
    return type(arg) in (int, str, Symbol)

def cons(head, pair):
    if is_atom(pair):
        pair = [pair]
    return tuple([head] + pair)

def make_vector(*args):
    _assert_pair(args)
    return Vector(args)

def more_than(left, right):
    _assert_int(left)
    _assert_int(right)
    return left > right

def less_than(left, right):
    _assert_int(left)
    _assert_int(right)
    return left < right

DUMMY = "dummy"
def dummy(*args):
    return DUMMY


BINDINGS = {
    Variable("eqv?"): Lambda((Variable('left'),Variable('right')), (PyFunction(eqv),), Context()),
    Variable("eq?"): Lambda((Variable('left'),Variable('right')), (PyFunction(eqv),), Context()),
    Variable("equal?"): Lambda((Variable('left'),Variable('right')), (PyFunction(equal),), Context()),
    Variable("number?"): Lambda((Variable('value'),), (PyFunction(number),), Context()),
    Variable('='): Lambda((Variable('values')), (PyFunction(number_eq),), Context()),
    Variable('+'): Lambda((Variable('args')), (PyFunction(plus),), Context()),
    Variable('-'): Lambda((Variable('args')), (PyFunction(minus),), Context()),
    Variable('>'): Lambda((Variable('left'),Variable('right')), (PyFunction(more_than),), Context()),
    Variable('<'): Lambda((Variable('left'),Variable('right')), (PyFunction(less_than),), Context()),
    Variable('list'): Lambda((Variable('args')), (PyFunction(_list),), Context()),
    Variable('make-vector'): Lambda((Variable('args')), (PyFunction(make_vector),), Context()),
    Variable('car'):Lambda((Variable('args'),), (PyFunction(car),), Context()),
    Variable('cdr'): Lambda((Variable('args'),), (PyFunction(cdr),), Context()),
    Variable('cons'): Lambda((Variable('head'),Variable('pair')), (PyFunction(cons),), Context()),
    Variable('atom?'): Lambda((Variable('arg'),), (PyFunction(is_atom),), Context()),
}
