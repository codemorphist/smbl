from .domain import Domain, DefaultDomain
from .operation import Operation, UnaryOperation, BinaryOperation
from .operation import OpVar, OpConst
from .operation import (Add, Sub, Mul, Div, 
                        FloorDiv, Mod, Pow)

from typing import Callable, Union


class OperationHandler:
    """
    Default operations for Var, Expression
    """
    def __is_const__(self, other) -> bool:
        """
        Check other is constant type
        """
        return isinstance(other, (int, float | complex))

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

    def __getattr__(cls, attr):
        return cls.get_var(attr)

    def exist(cls, var: str):
        """
        Check var is exist by name
        """
        return var is cls.__defined_vars__


class Var(OperationHandler, metaclass = VarMeta):
    """
    Variable class

    __new__: Create new varible and save it in storage of all variables
    __defined_vars__: dict[str, Var] Dict with every variable by name
    """
    __defined_vars__ = {}

    def __new__(cls, name, value: any=None, domain: Domain=DefaultDomain()):
        if name not in cls.__defined_vars__:
            self = super().__new__(cls)
            self._name = name
            
            if value is not None and not value in domain:
                raise ValueError(f"({value}) not in {domain}")

            self._value = value
            self._domain = domain

            cls.__defined_vars__[name] = self
        return cls.__defined_vars__[name]

    @classmethod
    def get_var(cls, name: str):
        """
        Return variable by name like attribute

        Usage example:
        >>> Var("x")
            Var("x", value=None, domain=DefaultDomain)
        >>> Var.get_var("x")        # by method get_var()
            Var("x", value=None, domain=DefaultDomain)
        >>> Var.x                   # syntax sugar by __getattr__ method
            Var("x", value=None, domain=DefaultDomain)
        >>> Var.x.value = 1
        >>> Var.x
            Var("x", value=1, domain=DefaultDomain)        
        """
        if name in cls.__defined_vars__:
            return cls.__defined_vars__[name]
        else:
            raise NameError(f"Variable with name ({name}) doesn't exist")

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
    def __init__(self, 
                 operation: Operation, 
                 vars: set[Var],
                 operands: list[any]):
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
            raise TypeError(f"Invalid type `{type(other).__name__}` to convert to Expression")

    @staticmethod
    def from_var(other: Var):
        return Expression(OpVar, {other}, [other])

    @staticmethod
    def from_const(other: Constant | int | float | complex):
        if isinstance(other, (int, float, complex)):
            other = Constant(other)
        return Expression(OpConst, set(), [other])

    @staticmethod
    def from_func(other: callable):
        # TODO
        # Extract variables names from fucntion (black box)
        vars = []
        for param in other.__code__.co_varnames:
            v = None
            if not Var.exist(param):
                v = Var(param)
            else:
                v = Var.getattr(param)
            vars.append(v)
        other._operand_count= other.__code__.co_argcount
        return Expression(other, {*vars}, [*vars])

    def __call__(self, **vars):
        """
        Calculate value of Expression or return new 
        Expression with replace given Vars values 
        to Constants
        
        If some Vars value not given return Expression,
        where Var with given values was replaced by 
        constant
        """
        for var in self._vars:
            if var.name not in vars:
                raise NameError(f"Variable `{var.name}` not given value")
            var.value = vars[var.name]

        if self._operation is OpVar or self._operation is OpConst:
            return self._operands[0]()

        operands = []
        for op in self._operands:
            if isinstance(op, Expression):
                operands.append(op(**vars))
            elif isinstance(op, Callable):
                # TODO
                pass
            else:
                raise TypeError(f"{type(op)} not valid type of operand")

        return self._operation(*operands)
   
    def composition(self, **params):
        pass

    def __repr__(self, ident: int=0) -> str:
        tab = "  "
        tabs = tab * ident
        operands_str = f"["
        for op in self._operands:
            operands_str += "\n"
            if isinstance(op, Expression):
                operands_str += op.__repr__(ident+1)
            elif isinstance(op, (Var, Constant)):
                operands_str += tabs + tab + repr(op)
            elif isinstance(op, Callable):
                operands_str += op.__name__
        operands_str += ","
        operands_str += "\n" + tabs + "]" 

        return f'{tabs}Expression(operation="{self._operation}", operands={operands_str})'

    def __str__(self) -> str:
        if self._operation is OpVar or self._operation is OpConst:
            return f"{self._operands[0]}"
        elif isinstance(self._operation, UnaryOperation): 
            return f"({self._operation} {self._operands[0]})"
        elif isinstance(self._operation, BinaryOperation):
            return f"({self._operands[0]} {self._operation} {self._operands[1]})"
        elif isinstance(self._operation, Callable):
            return f"{self._operation.__name__}({', '.join([str(op) for op in self._operands])})"
        else:
            operands = ", ".join(self._operands)
            return f"[{self._operation}]({operands})"

