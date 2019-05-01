from .model import Identifier, ProcedureCall, Variable, Lambda, StandardProcedure, Symbol, Definition, Program, Conditional, Vector, Quotation, Context, Let
from .stdproc import PROCEDURES

def execute(obj, context:Context):
    for t in (int, str, Symbol, Lambda, Vector):
        if isinstance(obj, t):
            return obj

    if type(obj) == tuple:
        return tuple((execute(x, context) for x in obj))

    elif isinstance(obj, ProcedureCall):
        return execute_procedure(obj, context)

    elif isinstance(obj, Variable):
        stdproc = StandardProcedure(obj.name)
        if stdproc in PROCEDURES:
            return stdproc
        if not obj in context.bindings:
            raise(Exception("variable {} not found".format(obj.name)))
        return context.bindings[obj]
    
    elif isinstance(obj, Definition):
        context.update_bindings(obj.variable, execute(obj.expression, context))
        return ()

    elif isinstance(obj, Program):
        result = ()
        for c in obj.commands:
            result = execute(c, context)
        return result
    
    elif isinstance(obj, Conditional):
        test = execute(obj.test, context)
        if test != False:
            return execute(obj.consequent, {})
        else:
            return execute(obj.alternate, {})

    elif isinstance(obj, Quotation):
        return obj.datum

    elif isinstance(obj, Let):
        for var, value in let_proc.bindings:
            context = context.bind_variable(var, execute(value, context))
        return execute(let_proc.body, context)


def execute_procedure(proc, context):
    operator = execute(proc.operator, context)
    operand = tuple((execute(a, context) for a in proc.operand))

    if operator in PROCEDURES:
        return PROCEDURES[operator](*operand)
    if isinstance(operator, Lambda):
        if len(operand) > len(operator.formals):
            raise(Exception("wrong number of arguments {} for {}".format(operand, proc)))
        for i, o in enumerate(operand):
            context = context.bind(operator.formals[i], o)
        body = [execute(b, context) for b in operator.body]
        if len(operand) == len(operator.formals):
            # closed expression
            return body[-1]
        else:
            # curry-ing
            return Lambda(operator.formals[len(operand):], tuple(body))
    else:
        raise(Exception("undefined procedure {}".format(operator)))
