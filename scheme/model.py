from dataclasses import dataclass
from typing import Callable, Union, Tuple

# type alias
class Lambda: pass
class Vector: pass
class Character: pass
class Variable: pass
class Quotation: pass
class Conditional: pass
class Cond: pass
class Or: pass
class And: pass
Expression = Union[str, int, tuple, Lambda, Vector, Character, Variable, Quotation, Conditional, Cond]


@dataclass()
class Context:
    bindings: dict
    def __init__(self, bindings={}):
        self.bindings = bindings
    
    def bind(self, variable, value):
        new_context = self.copy()
        new_context.bindings[variable] = value
        return new_context
    
    def update_bindings(self, variable, value):
        self.bindings[variable] = value
   
    def copy(self):
        return Context(self.bindings.copy())


@dataclass(frozen=True)
class Symbol:
    name: str


@dataclass(frozen=True)
class Variable:
    name: str

    def execute(self, context, execute):
        if not self in context.bindings:
            raise(Exception("variable {} not found".format(self.name)))
        return context.bindings[self]


@dataclass
class Lambda:
    formals: tuple
    body: tuple
    context: Context

    def execute(self, context:Context, execute):
        # capture variables (closure)
        return Lambda(self.formals, self.body, context.copy())


@dataclass(frozen=True)
class ProcedureCall:
    operator: Lambda
    operand: tuple

    def execute_closed_function(self, operator, context, execute):
        if isinstance(operator.body, PyFunction):
            formals = operator.formals
            if isinstance(formals, SingleParameter):
                return operator.body.function(context.bindings[formals.name])
            elif isinstance(formals, FixedParameters):
                return operator.body.function(**{k.name:context.bindings[k] for k in formals.names})
            elif isinstance(formals, ParametersWithLast):
                args = [context.bindings[k] for k in list(formals.names)]
                args += context.bindings[formals.last]
                print(args)
                return operator.body.function(*args)
            else:
                raise(Exception("unexpected type {} as parameter definition".format(type(formals))))
        else:
            results = [execute(command, context) for command in operator.body]
            return results[-1]


    def execute(self, context, execute):
        operator = execute(self.operator, context)
        operand = tuple((execute(a, context) for a in self.operand))

        if not isinstance(operator, Lambda):
            raise(Exception("undefined procedure {}".format(operator)))

        inner_context = operator.context.copy()
        formals = operator.formals
        if isinstance(formals, SingleParameter):
            inner_context = inner_context.bind(formals.name, operand if len(operand) != 1 else operand[0])
            return self.execute_closed_function(operator, inner_context, execute)
        elif isinstance(formals, FixedParameters):
            if len(operand) > len(formals.names):
                raise(Exception("wrong number of arguments {} for {}".format(operand, self)))
            for i,o in enumerate(operand):
                inner_context = inner_context.bind(formals.names[i], o)
            if len(operand) == len(formals.names):
                return self.execute_closed_function(operator, inner_context, execute)
            else:
                # curry-ing
                return execute(Lambda(FixedParameter(tuple(formals.names[len(operand):])), operator.body), inner_context)
        elif isinstance(formals, ParametersWithLast):
            print(operand)
            if len(operand) < len(formals.names):
                # curry-ing
                for i,o in enumerate(operand):
                    inner_context = inner_context.bind(formals.names[i], o)
                return execute(Lambda(ParametersWithLast(tuple(formals.names[len(operand):]), formals.last), operator.body), inner_context)
            else:
                for i,name in enumerate(formals.names):
                    inner_context = inner_context.bind(name, operand[i])
                inner_context = inner_context.bind(formals.last, operand[len(formals.names):])
                return self.execute_closed_function(operator, inner_context, execute)
        else:
            raise(Exception("BUG: invalid parameter type: {}".format(type(formals))))


@dataclass(frozen=True)
class SingleParameter:
    name: str


@dataclass(frozen=True)
class FixedParameters:
    names: str


@dataclass(frozen=True)
class ParametersWithLast:
    names: tuple
    last: str


@dataclass(frozen=True)
class Vector:
    values: tuple


@dataclass(frozen=True)
class Character:
    value: str


@dataclass
class Definition:
    variable: Variable
    expression : Expression

    def execute(self, context, execute):
        context.update_bindings(self.variable, execute(self.expression, context))
        return ()


@dataclass
class Program:
    commands: tuple

    def execute(self, context, execute):
        result = ()
        for c in self.commands:
            result = execute(c, context)
        return result


@dataclass
class Conditional:
    test: Expression
    consequent: Expression
    alternate: Expression

    def execute(self, context, execute):
        test = execute(self.test, context)
        if test != False:
            return execute(self.consequent, context)
        else:
            return execute(self.alternate, context)


@dataclass
class Let:
    bindings: tuple
    body: Expression

    def execute(self, context, execute):
        for var, value in self.bindings:
            context = context.bind(var, execute(value, context))
        return execute(self.body, context)[-1]


@dataclass
class Set_:
    variable: Variable
    expression: Expression

    def execute(self, context, execute):
        context.update_bindings(self.variable, execute(self.expression, context))


@dataclass
class CondClause:
    test: Expression
    expressions: Tuple[Expression] = ()
    is_call: bool = False

@dataclass()
class Cond:
    clauses: Tuple[CondClause]

    def execute(self, context, execute):
        for clause in self.clauses:
            ret = execute(clause.test, context)
            if ret is False:
                continue
            if len(clause.expressions) == 0:
                return ret
            if clause.is_call:
                return execute(ProcedureCall(clause.expressions[0], (ret,)), context)
            else:
                results = [execute(e, context) for e in clause.expressions]
                return results[-1]
        # no match
        return ()


@dataclass()
class And:
    expressions: Tuple[Expression]

    def execute(self, context, execute):
        ret = True
        for expression in self.expressions:
            ret = execute(expression, context)
            if ret is False:
                return ret
        return ret


@dataclass()
class Or:
    expressions: Tuple[Expression]

    def execute(self, context, execute):
        ret = False
        for expression in self.expressions:
            ret = execute(expression, context)
            if ret is not False:
                return ret
        return ret
 
@dataclass(frozen=True)
class PyFunction:
   function: Callable[..., Expression]
