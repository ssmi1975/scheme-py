from .model import *

def execute(obj, context:Context):
    for t in (int, str, Symbol, Vector):
        if isinstance(obj, t):
            return obj

    if type(obj) == tuple:
        return tuple((execute(x, context) for x in obj))

    return obj.execute(context, execute)
