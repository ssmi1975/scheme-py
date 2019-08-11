from __future__ import annotations
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

class Context(dict):
    def bind(self, variable, value):
        new_context = self.copy()
        new_context[variable] = value
        return new_context
    
    def update_bindings(self, variable, value):
        self[variable] = value
    
    def copy(self):
        return Context(self)


@dataclass(frozen=True)
class Symbol:
    name: str


@dataclass(frozen=True)
class Variable:
    name: str

    def execute(self, context, execute):
        if not self in context:
            raise(Exception("variable {} not found".format(self.name)))
        return context[self]


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

    def execute_closed_function(self, body, context, execute):
        if isinstance(body, PyFunction):
            return body.execute(context, execute)
        else:
            results = [execute(command, context) for command in body]
            return results[-1]


    def execute(self, context, execute):
        operator = execute(self.operator, context)
        operand = tuple((execute(a, context) for a in self.operand))

        if not isinstance(operator, Lambda):
            raise(Exception("undefined procedure {}".format(operator)))

        formals = operator.formals
        inner_context = operator.context.copy()
        inner_context = formals.bind_context(operand, inner_context)
        if formals.is_closed(operand):
            return self.execute_closed_function(operator.body, inner_context, execute)
        else:
            return Lambda(formals.curry(operand), operator.body, inner_context)


@dataclass(frozen=True)
class SingleParameter:
    name: str

    def is_closed(self, operand):
        return True

    def bind_context(self, operand, context):
        return context.bind(self.name, operand if len(operand) != 1 else operand[0])

    def curry(self, operand):
        raise(Exception("BUG: curry called for {}".format(self.__class__)))


@dataclass(frozen=True)
class FixedParameters:
    names: str

    def is_closed(self, operand):
        if len(operand) > len(self.names):
            raise(Exception("wrong number of arguments {} for {}".format(operand, self)))
        else:
            return len(operand) == len(self.names)
        
    def bind_context(self, operand, context):
        for i,o in enumerate(operand):
            context = context.bind(self.names[i], o)
        return context

    def curry(self, operand):
        return FixedParameter(tuple(self.names[len(operand):]))


@dataclass(frozen=True)
class ParametersWithLast:
    names: tuple
    last: str

    def is_closed(self, operand):
        return len(operand) >= len(self.names)

    def bind_context(self, operand, context):
        if len(operand) < len(self.names):
            for i,o in enumerate(operand):
                context = context.bind(self.names[i], o)
            return context
        else:
            for i,name in enumerate(self.names):
                context = context.bind(name, operand[i])
            context = context.bind(self.last, operand[len(self.names):])
            return context

    def curry(self, operand):
        return ParametersWithLast(tuple(self.names[len(operand):]))

    def arg_for_pyfunction(self, context):
        return context[self.name]


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
    formals: tuple = ()

    def execute(self, context, execute):
        if isinstance(self.formals, SingleParameter):
            return self.function(context[self.formals.name])
        elif isinstance(self.formals, FixedParameters):
            return self.function(**{k.name:context[k] for k in self.formals.names})
        elif isinstance(self.formals, ParametersWithLast):
            args = [context[k] for k in list(self.formals.names)]
            args += context[self.formals.last]
            return self.function(*args)
        else:
            raise(Exception("unexpected type {} as parameter definition".format(type(self.formals))))

@dataclass(frozen=True)
class Ellipsis:
    name: str = "..."

@dataclass(frozen=True)
class PatternDatum:
    value: Union[int, Character, str, bool]

@dataclass(frozen=True)
class Template:
    children: Tuple[Union[PatternDatum, Symbol, ]] = ()
    has_ellipsis: bool = False  # does this template has "..."?
    capture_last: bool = False  # the last children captures the last items " . t"?

@dataclass(frozen=True)
class Pattern:
    children: tuple = ()
    has_ellipsis: bool = False  # does this template has "..."?
    capture_last: bool = False  # the last children captures the last items " . t"?
    
@dataclass(frozen=True)
class SyntaxRule:
    pattern: Pattern
    template: Template

@dataclass(frozen=True)
class TransformerSpec:
    identifiers: tuple
    syntax_rules: tuple

@dataclass(frozen=True)
class SyntaxDefinition:
    name: Symbol
    spec: TransformerSpec
