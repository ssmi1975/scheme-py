from .model import Identifier, Symbol, Variable, StandardProcedure, Vector
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

def plus(*args):
    if not all((isinstance(arg, int) for arg in args)):
        raise(Exception("non-number value(s) are passed: {}".format(args)))
    return sum(args)

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

def cdr(arg):
    _assert_pair(arg)
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


PROCEDURES = {
    StandardProcedure('eqv?'): eqv,
    StandardProcedure('eq?'): eqv,
    StandardProcedure('equal?'): equal,
    StandardProcedure('number?'): number,
    StandardProcedure('number?'): number,
    StandardProcedure('='): number_eq,
    StandardProcedure('+'): plus,
    StandardProcedure('>'): more_than,
    StandardProcedure('<'): less_than,
    StandardProcedure('list'): _list,
    StandardProcedure('make-vector'): make_vector,
    StandardProcedure('car'): car,
    StandardProcedure('cdr'): car,
    StandardProcedure('cons'): cons,
    StandardProcedure('atom?'): is_atom,
}