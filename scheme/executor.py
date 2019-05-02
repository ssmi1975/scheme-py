from .model import Identifier, ProcedureCall, Variable, Lambda, Symbol, Definition, Program, Conditional, Vector, Quotation, Context, Let, PyFunction

def execute(obj, context:Context):
    for t in (int, str, Symbol, Vector):
        if isinstance(obj, t):
            return obj

    if type(obj) == tuple:
        return tuple((execute(x, context) for x in obj))

    elif isinstance(obj, Lambda):
        return execute_lambda(obj, context)

    elif isinstance(obj, ProcedureCall):
        return execute_procedure(obj, context)

    elif isinstance(obj, Variable):
        if obj in context.parameters:
            return obj
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

def execute_lambda(lambda_def:Lambda, context):
    # capture variables (closure)
    return Lambda(lambda_def.formals, lambda_def.body, context.copy())


def execute_procedure(proc, context):
    operator = execute(proc.operator, context)
    operand = tuple((execute(a, context) for a in proc.operand))

    if isinstance(operator, Lambda):
        if len(operand) > len(operator.formals):
            raise(Exception("wrong number of arguments {} for {}".format(operand, proc)))
        inner_context = operator.context.copy()
        for i,o in enumerate(operand):
            inner_context = inner_context.bind(operator.formals[i], operand[i])
        if isinstance(operator.body, PyFunction):
            obj.function(**context)
        body = [execute(b, inner_context) for b in operator.body]
        if len(operand) == len(operator.formals):
            # closed expression
            return body[-1]
        else:
            # curry-ing
            return Lambda(operator.formals[len(operand):], tuple(body), operator.context)
    else:
        raise(Exception("undefined procedure {}".format(operator)))
