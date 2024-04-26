from .domain import Domain, DefaultDomain
from .operation import Operation, UnaryOperation, BinaryOperation
from .operation import OpVar, OpConst
from .operation import Add, Sub, Mul, Div, FloorDiv, Mod, Pow

from typing import Callable, Union
import math


class OperationHandler:
    """
    Default operations for Var, Expression
    """

    def __is_const__(self, other) -> bool:
        """
        Check other is constant type
        """
        return isinstance(other, (int, float, complex))

    def __add__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Add, self.vars | other.vars, [self, other])

    def __sub__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Sub, self.vars | other.vars, [self, other])

    def __mul__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Mul, self.vars | other.vars, [self, other])

    def __truediv__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Div, self.vars | other.vars, [self, other])

    def __floordiv__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(FloorDiv, self.vars | other.vars, [self, other])

    def __mod__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Mod, self.vars | other.vars, [self, other])

    def __pow__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Pow, self.vars | other.vars, [self, other])

    def __radd__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Add, self.vars | other.vars, [other, self])

    def __rsub__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Sub, self.vars | other.vars, [other, self])

    def __rmul__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Mul, self.vars | other.vars, [other, self])

    def __rpow__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Pow, self.vars | other.vars, [other, self])

    def __rtruediv__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(Div, self.vars | other.vars, [other, self])

    def __rfloordiv__(self, other):
        other = Expression.to_expression(other)
        self = Expression.to_expression(self)
        return Expression(FloorDiv, self.vars | other.vars, [other, self])


class Constant(OperationHandler):
    def __init__(self, value: Union[int, float, complex]):
        self._value = value

    def __call__(self):
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Constant(type={type(self._value).__name__}, value={self._value})"


class VarMeta(type):
    """
    Metaclass for syntax sugar of Var

    Example:
    >>> Var("x")        # create (register) new variable
        Var("x", value=None, domain=DefaultDomain)
    >>> Var.x           # get variable without saving pointer to this variable
        Var("x", value=None, domain=DefaultDomain)
    """

    def __getattr__(cls, var_name):
        if not cls.exist(var_name):
            raise NameError(f"Variable with name `{var_name}` not exist")
        return cls.__defined_vars__[var_name]

    def exist(cls, var: str):
        """
        Check var is exist by name
        """
        return var in cls.__defined_vars__


class Var(OperationHandler, metaclass=VarMeta):
    """
    Variable class

    __defined_vars__: dict[str, Var] Dict with every variable by name
    """

    __defined_vars__ = {}

    def __new__(cls, name, value: any = None, domain: Domain = DefaultDomain()):
        """
        Singleton pattern

        Create new varible and save it in storage of all variables
        """
        if name not in cls.__defined_vars__:
            self = super().__new__(cls)
            self._name = name

            if value is not None and value not in domain:
                raise ValueError(f"({value}) not in {domain}")

            self._value = value
            self._domain = domain

            cls.__defined_vars__[name] = self
        return cls.__defined_vars__[name]

    def __call__(self) -> any:
        return self.value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> any:
        return self._value

    @value.setter
    def value(self, val: any):
        if val in self._domain:
            self._value = val
        else:
            raise ValueError(f"({val}) not in {self.domain}")

    @property
    def domain(self):
        return self._domain

    def __repr__(self) -> str:
        return f'Var("{self.name}", value={self.value}, domain={self.domain})'

    def __str__(self) -> str:
        return self.name

    def __hash__(self):
        return hash(self._name)

    def __set__(self, other):
        self.value = other


class Expression(OperationHandler):
    def __init__(self, operation: Operation, vars: set[Var], operands: list[any]):
        """
        :param operation: Operation for Expression, CONST, VAR return value of Var
                          or Constant
        :params vars: varibles used in Expression
        :params operands: operands in Expression
        """
        self._vars = vars
        self._operation = operation
        self._operands = operands

    @property
    def vars(self) -> set[Var]:
        """
        Return set of vars using in Expression
        """
        return self._vars

    @staticmethod
    def to_expression(other):
        if isinstance(other, Var):
            return Expression.from_var(other)
        elif isinstance(other, (Constant, int, float, complex)):
            return Expression.from_const(other)
        elif isinstance(other, Expression):
            return other
        elif isinstance(other, Callable):
            return Expression.from_func(other)
        else:
            raise TypeError(
                f"Invalid type `{type(other).__name__}` to convert to Expression"
            )

    @staticmethod
    def from_var(var: Var):
        return Expression(OpVar, {var}, [var])

    @staticmethod
    def from_const(const: Union[Constant, int, float, complex]):
        if isinstance(const, (int, float, complex)):
            const = Constant(const)
        return Expression(OpConst, set(), [const])

    @staticmethod
    def from_func(func: Callable):
        # TODO
        # NOTE: Use func.__code__.co_varnames to get function parameters
        vars = []
        for v in func.__code__.co_varnames:
            if Var.exist(v):
                var = getattr(Var, v)
            else:
                var = Var(v)
            vars.append(var)
        return Expression(func, set(vars), vars)

    @staticmethod
    def from_callable(func: Callable, vars: set[Var]):
        return Expression(func, vars, [*vars])

    def __call__(self, **vars):
        """
        Calculate value of Expression or return new
        Expression with replace given Vars values
        to constant
        """
        for var in self._vars:
            if var.name not in vars:
                raise NameError(f"Variable `{var.name}` not given value")
            var.value = vars[var.name]

        # if operation is OpVar of OpConst return only value
        if self._operation is OpVar or self._operation is OpConst:
            return self._operands[0]()

        operands = []
        for op in self._operands:
            if isinstance(op, Expression):
                operands.append(op(**vars))
            elif isinstance(op, Var):
                operands.append(op())
            else:
                raise TypeError(f"{type(op)} not valid type of operand")

        return self._operation(*operands)

    def substitude(self, **params):
        operands = []
        vars = self.vars
        for op in self._operands:
            if isinstance(op, Expression):
                new_expr = op.substitude(**params)
                vars |= new_expr.vars
                operands.append(new_expr)
            elif isinstance(op, Var) and op.name in params:
                value = params[op.name]
                if isinstance(value, (int, float, complex)):
                    value = Constant(value)
                elif not isinstance(value, (Var, Expression)):
                    raise TypeError(
                        f"Invalid type {type(value)} to substitude Expression"
                    )
                operands.append(value)
            else:
                operands.append(op)
        return Expression(self._operation, vars, operands)

    def derivative(self, var: Var):
        if self._operation not in [Add, Sub, Mul, Div, Pow, OpVar, OpConst]:
            raise Exception(f"Invalid operation {self._operation} to take derivative")
        if var not in self._vars:
            return Expression.to_expression(0)

        if self._operation is OpVar:
            return Expression.to_expression(1)
        elif self._operation is OpConst:
            return Expression.to_expression(0)

        f, g = self._operands
        fd = self._derivative(f, var)
        gd = self._derivative(g, var)

        x = Var("x") if not Var.exist("x") else Var.x
        ln = Expression.from_callable(math.log, {x})

        if self._operation is Add:
            return fd + gd
        elif self._operation is Sub:
            return fd - gd
        elif self._operation is Mul:
            return f * gd + g * fd
        elif self._operation is Div:
            return (f * gd - g * fd) / g**2
        elif self._operation is Pow:
            return f**g * (gd * ln.substitude(x=f) + g / f)

    def _derivative(self, expr: any, var: Var):
        if isinstance(expr, Expression):
            return expr.derivative(var)
        elif isinstance(expr, Var) and expr is var:
            return Expression.to_expression(1)
        else:
            return Expression.to_expression(0)

    def __repr__(self, ident: int = 0) -> str:
        tab = "  "
        tabs = tab * ident
        operands_str = "["
        for op in self._operands:
            operands_str += "\n"
            if isinstance(op, Expression):
                operands_str += op.__repr__(ident + 1)
            elif isinstance(op, (Var, Constant)):
                operands_str += tabs + tab + repr(op)
            elif isinstance(op, Callable):
                # TODO
                pass
        operands_str += ","
        operands_str += "\n" + tabs + "]"

        return (
            f'{tabs}Expression(operation="{self._operation}", operands={operands_str})'
        )

    def __str__(self) -> str:
        if self._operation is OpVar or self._operation is OpConst:
            return f"{self._operands[0]}"
        elif isinstance(self._operation, UnaryOperation):
            return f"({self._operation} {self._operands[0]})"
        elif isinstance(self._operation, BinaryOperation):
            return f"({self._operands[0]} {self._operation} {self._operands[1]})"
        elif isinstance(self._operation, Callable):
            vars = ", ".join(str(v) for v in self._operands)
            return f"{self._operation.__name__}({vars})"
        else:
            operands = ", ".join(self._operands)
            return f"[{self._operation}]({operands})"
