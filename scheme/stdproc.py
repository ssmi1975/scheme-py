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

def car(*args):
    _assert_pair(args)
    return tuple(args[0])

def make_vector(*args):
    _assert_pair(args)
    return Vector(args)

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
    StandardProcedure('list'): _list,
    StandardProcedure('make-vector'): make_vector,
    StandardProcedure('car'): car,
}