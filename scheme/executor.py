from .model import (ProcedureCall, Variable, Lambda, Symbol, Definition, Program, Conditional, Vector,
 Quotation, Context, Let, PyFunction, SingleParameter, FixedParameters, ParametersWithLast)

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
        for var, value in obj.bindings:
            context = context.bind(var, execute(value, context))
        return execute(obj.body, context)[-1]

def execute_lambda(lambda_def:Lambda, context):
    # capture variables (closure)
    return Lambda(lambda_def.formals, lambda_def.body, context.copy())

def execute_closed_function(operator, context):
    if isinstance(operator.body, PyFunction):
        formals = operator.formals
        if isinstance(formals, SingleParameter):
            return operator.body.function(context.bindings[formals.name])
        elif isinstance(formals, FixedParameters):
            return operator.body.function(**{k.name:context.bindings[k] for k in formals.names})
        elif isinstance(formals, ParametersWithLast):
            args = {k.name:context.bindings[k] for k in formals.names + [formals.last]}
            return operator.body.function(*args)
        else:
            raise(Exception("unexpected type {} as parameter definition".format(type(formals))))
    else:
        results = [execute(command, context) for command in operator.body]
        return results[-1]

def execute_procedure(proc, context):
    operator = execute(proc.operator, context)
    operand = tuple((execute(a, context) for a in proc.operand))

    if not isinstance(operator, Lambda):
        raise(Exception("undefined procedure {}".format(operator)))

    inner_context = operator.context.copy()
    formals = operator.formals
    if isinstance(formals, SingleParameter):
        inner_context = inner_context.bind(formals.name, operand if len(operand) != 1 else operand[0])
        return execute_closed_function(operator, inner_context)
    elif isinstance(formals, FixedParameters):
        if len(operand) > len(formals.names):
            raise(Exception("wrong number of arguments {} for {}".format(operand, proc)))
        for i,o in enumerate(operand):
            inner_context = inner_context.bind(formals.names[i], o)
        if len(operand) == len(formals.names):
            return execute_closed_function(operator, inner_context)
        else:
            # curry-ing
            return execute(Lambda(FixedParameter(tuple(formals.names[len(operand):])), operator.body), inner_context)
    elif isinstance(formals, ParametersWithLast):
        raise(NotImplementedError(""))
    else:
        raise(Exception("BUG: invalid parameter type: {}".format(type(formals))))