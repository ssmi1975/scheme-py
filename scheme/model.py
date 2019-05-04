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

@dataclass
class Lambda:
    formals: tuple
    body: tuple
    context: Context

@dataclass(frozen=True)
class ProcedureCall:
    operator: Lambda
    operand: tuple

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

@dataclass
class Program:
   commands: tuple

@dataclass
class Conditional:
    test: Expression
    consequent: Expression
    alternate: Expression

@dataclass
class Quotation:
    datum: Expression

@dataclass
class Let:
    bindings: tuple
    body: Expression

@dataclass
class Set_:
    variable: Variable
    expression: Expression

@dataclass
class CondClause:
    test: Expression
    expressions: Tuple[Expression] = ()
    is_call: bool = False

@dataclass()
class Cond:
    clauses: Tuple[CondClause]

@dataclass(frozen=True)
class PyFunction:
   function: Callable[..., Expression]
