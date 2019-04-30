from .model import Identifier, ProcedureCall, Variable, Lambda, StandardProcedure, Symbol, Definition, Program, Conditional, Vector, Quotation
from .stdproc import PROCEDURES

def execute(obj, context):
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
        if not obj in context:
            raise(Exception("variable {} not found".format(obj.name)))
        return context[obj]
    
    elif isinstance(obj, Definition):
        new_context = bind_variable(context, obj.variable, execute(obj.expression, context))
        context.update(new_context)
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




def bind_variable(context, variable, value):
    print("binding {} to {}".format(variable, value))
    new_context = context.copy()
    new_context[variable] = value
    return new_context

def execute_let(let_proc, context):
    context = bind_variable()
    for var, value in let_proc.operand[0]:
        context = bind_variable(var, value)
    return execute(let_proc.body, context)

LETS = {
    Variable('let'): execute_let,
}

def execute_procedure(proc, context):
    operator = execute(proc.operator, context)
    operand = tuple((execute(a, context) for a in proc.operand))
    if operator in LETS:
        return LETS[operator](proc, context)

    if operator in PROCEDURES:
        return PROCEDURES[operator](*operand)
    if isinstance(operator, Lambda):
        if len(operand) > len(operator.formals):
            raise(Exception("wrong number of arguments {} for {}".format(operand, proc)))
        for i, o in enumerate(operand):
            context = bind_variable(context, operator.formals[i], o)
        body = [execute(b, context) for b in operator.body]
        if len(operand) == len(operator.formals):
            # closed expression
            return body[-1]
        else:
            # curry-ing
            return Lambda(operator.formals[len(operand):], tuple(body))
    else:
        raise(Exception("undefined procedure {}".format(operator)))
