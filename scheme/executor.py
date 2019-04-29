from .model import Identifier, ProcedureCall, Variable, Lambda, StandardProcedure, Symbol
from .stdproc import PROCEDURES

def execute(obj, context):
    for t in (int, str, Symbol, Lambda):
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


def bind_variable(context, variable, value):
    print("binding {} to {}".format(variable, value))
    new_context = context.copy()
    new_context[variable] = value
    return new_context


def execute_procedure(proc, context):
    operator = execute(proc.operator, context)
    operand = tuple((execute(a, context) for a in proc.operand))
    if operator in PROCEDURES:
        return PROCEDURES[operator](*operand)
    if isinstance(operator, Lambda):
        print(operator.formals)
        if len(operand) > len(operator.formals):
            raise(Exception("wrong number of arguments {} for {}".format(operand, proc)))
        for i, o in enumerate(operand):
            context = bind_variable(context, operator.formals[i], o)
        if len(operand) == len(operator.formals):
            return execute(operator.body, context)
        else:
            return Lambda(operator.formals[len(operand):], execute(operator.body, context))
    else:
        raise(Exception("undefined procedure {}".format(operator)))
