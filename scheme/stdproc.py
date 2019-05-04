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


BINDINGS = {
    Variable("eqv?"): Lambda(FixedParameters((Variable('left'),Variable('right'))), PyFunction(eqv), Context()),
    Variable("eq?"): Lambda(FixedParameters((Variable('left'),Variable('right'))), PyFunction(eqv), Context()),
    Variable("equal?"): Lambda(FixedParameters((Variable('left'),Variable('right'))), PyFunction(equal), Context()),
    Variable("number?"): Lambda(FixedParameters((Variable('value'),)), PyFunction(number), Context()),
    Variable('='): Lambda(SingleParameter(Variable('values')), PyFunction(number_eq), Context()),
    Variable('+'): Lambda(SingleParameter(Variable('args')), PyFunction(plus), Context()),
    Variable('-'): Lambda(ParametersWithLast((Variable('first'),), Variable('last')), PyFunction(minus), Context()),
    Variable('>'): Lambda(FixedParameters((Variable('left'),Variable('right'))), PyFunction(more_than), Context()),
    Variable('<'): Lambda(FixedParameters((Variable('left'),Variable('right'))), PyFunction(less_than), Context()),
    Variable('list'): Lambda(SingleParameter(Variable('args')), PyFunction(_list), Context()),
    Variable('make-vector'): Lambda(SingleParameter(Variable('args')), PyFunction(make_vector), Context()),
    Variable('car'):Lambda(FixedParameters((Variable('args'),)), PyFunction(car), Context()),
    Variable('cdr'): Lambda(FixedParameters((Variable('args'),)), PyFunction(cdr), Context()),
    Variable('cons'): Lambda(FixedParameters((Variable('head'),Variable('pair'))), PyFunction(cons), Context()),
    Variable('atom?'): Lambda(FixedParameters((Variable('arg'),)), PyFunction(is_atom), Context()),
    Variable('quote'): Lambda(FixedParameters((Variable('datum'),)), PyFunction(quote), Context()),
}

# vim: expandtab sw=4 sts=4
