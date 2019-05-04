from scheme.model import *
from scheme.stdproc import BINDINGS

def procedure(name, *args):
    return ProcedureCall(Variable(name), args)

def quote(args):
    return procedure('quote', args)

def default_context(extra_bindings={}):
    c = Context(BINDINGS)
    for k,v in extra_bindings.items():
        c = c.bind(k, v)
    return c

def t_(*args):
    return args
    