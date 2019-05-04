from .model import *
import collections

def eqv(left, right):
    for t in (Symbol, Variable, int):
        if isinstance(left, t) and isinstance(right, t):
            return left == right
    if left == () and right == ():
        return True
    return left is right

def equal(left, right):
    print("{}, {}".format(left, right))
    return left == right

def number(value):
    return type(value) == int

def number_eq(values):
    if type(values) == int:
        return True
    return all((values[0] == v for v in values))

def _assert_all_int(args):
    if not all((isinstance(arg, int) for arg in args)):
        raise(Exception("non-number value(s) are passed: {}".format(args)))

def plus(args:tuple):
    _assert_all_int(args)
    return sum(args)

def minus(first:int, *last:tuple):
    assert type(first) == int
    _assert_all_int(last)
    if len(last) == 0:
        return first
    else:
        return first - sum(last)

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

def car(args:tuple):
    _assert_non_empty_pair(args)
    return tuple(args[0])

def cdr(args:tuple):
    _assert_pair(args)
    _assert_non_empty_pair(args)
    return tuple(args[1:])

def is_atom(arg):
    return type(arg) in (int, str, Symbol)

def cons(head, pair:tuple):
    if is_atom(pair):
        pair = [pair]
    return tuple([head] + pair)

def make_vector(args:tuple):
    _assert_pair(args)
    return Vector(args)

def more_than(left:int, right:int):
    _assert_int(left)
    _assert_int(right)
    return left > right

def less_than(left:int, right:int):
    _assert_int(left)
    _assert_int(right)
    return left < right

def quote(datum):
    return datum

def _t(*args):
    # tuple of variables
    return tuple(Variable(v) for v in args)

def _v(name):
    # variable with given name
    return Variable(name)

def py_function(func, formals):
    return Lambda(formals, PyFunction(func, formals), Context())

BINDINGS = {
    Variable("eqv?"): py_function(eqv, FixedParameters(_t('left', 'right'))),
    Variable("eq?"): py_function(eqv, FixedParameters(_t('left', 'right'))),
    Variable("equal?"): py_function(equal, FixedParameters(_t('left', 'right'))),
    Variable("number?"): py_function(number, FixedParameters( _t('value'))),
    Variable('='): py_function(number_eq, SingleParameter(_v('values'))),
    Variable('+'): py_function(plus, SingleParameter(_v('args'))),
    Variable('-'): py_function(minus, ParametersWithLast( _t('first'), _v('last'))),
    Variable('>'): py_function(more_than, FixedParameters( _t('left' ,'right'))),
    Variable('<'): py_function(less_than, FixedParameters( _t('left', 'right'))),
    Variable('list'): py_function(_list, SingleParameter(_v('args'))),
    Variable('make-vector'): py_function(make_vector, SingleParameter(_v('args'))),
    Variable('car'): py_function(car, FixedParameters( _t('args'))),
    Variable('cdr'): py_function(cdr, FixedParameters( _t('args'))),
    Variable('cons'): py_function(cons, FixedParameters( _t('head','pair'))),
    Variable('atom?'): py_function(is_atom, FixedParameters( _t('arg'))),
    Variable('quote'): py_function(quote, FixedParameters( _t('datum'))),
}

# vim: expandtab sw=4 sts=4
