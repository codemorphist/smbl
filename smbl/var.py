from .domain import Domain, DefaultDomain
from .operation import Operation
from .operation import (Add, Sub, Mul, Div, 
                        FloorDiv, Mod, Pow)

from typing import Union


class OperationHandler:
    """
    Default operations for Var, Expression
    """
    def __is_const__(self, other) -> bool:
        """
        Check other is constant type
        """
        return isinstance(other, int | float | complex)

    def __add__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Add, self.vars | other.vars, self, other)

    def __sub__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Sub, self.vars | other.vars, self, other)

    def __mul__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Mul, self.vars | other.vars, self, other)

    def __truediv__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Div, self.vars | other.vars, self, other)

    def __floordiv__(self, other):
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(FloorDiv, self.vars | other.vars, self, other)

    def __mod__(self, other):
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Mod, self.vars | other.vars, self, other)

    def __pow__(self, other):
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Pow, self.vars | other.vars, self, other)

    def __radd__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Add, self.vars | other.vars, other, self)

    def __rsub__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Sub, self.vars | other.vars, other, self)

    def __rmul__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Mul, self.vars | other.vars, other, self)

    def __rtruediv__(self, other): 
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(Div, self.vars | other.vars, other, self)

    def __rfloordiv__(self, other):
        if self.__is_const__(other):
            other = Constant(other)
        return Expression(FloorDiv, self.vars | other.vars, other, self)

    @property
    def vars(self):
        return self._vars


class Constant(OperationHandler):
    def __init__(self, value: Union[int, float, complex]):
        self._value = value
        self._vars = set()

    def __call__(self, *args, **kwargs):
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
            self._vars = set([self])

            cls.__defined_vars__[name] = self
        else:
            raise NameError(f"Variable with name ({name}) alredy exist")
        return cls.__defined_vars__[name]

    @classmethod
    def get_var(cls, name: str):
        """
        Return variable by name

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

    def __call__(self, **values) -> any:
        if self.name in values:
            return values[self.name]
        elif self.value is not None:
            return self.value
        else:
            return self

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


class Expression(OperationHandler):
    def __init__(self, 
                 operation: Operation, 
                 vars: list[Var],
                 *operands: list[any]):
        self._vars = vars
        self._operation = operation

        if len(operands) > operation._operand_count:
            raise Exception("Too many operands for operation")
        elif len(operands) < operation._operand_count:
            raise Exception("Not enought operands for operation")
        else:
            self._operands = operands

        # convert int, float or complex to Constant class
        for i, op in enumerate(self._operands):
            if isinstance(op, int | float | complex):
                self._operands[i] = Constant(op)

    def __call__(self, **vars):
        """
        Calculate value of Expression or return new 
        Expression with replace given Vars values 
        to Constants
        
        If some Vars value not given return Expression,
        where Var with given values was replaced by 
        constant
        """
        # Deprecated
        # for var, value in vars.items():
            # var = getattr(Var, var)
            # var.value = value

        new_operands = []
        for op in self._operands:
            if isinstance(op, Constant):
                new_operands.append(op)
            elif isinstance(op, Var):
                new_operands.append(op(**vars))
            elif isinstance(op, Expression):
                # If Expression calculate value recursively
                new_operands.append(op(**vars))
            else:
                raise TypeError(f"{type(op)} not valid type for calculate Expression")

        return self._operation(*new_operands)
   
    def __repr__(self, ident: int=0) -> str:
        tab = "  "
        tabs = tab * ident
        operands_str = f"["
        for op in self._operands:
            operands_str += "\n"
            if isinstance(op, Expression):
                operands_str += op.__repr__(ident+1)
            else:
                operands_str += tabs + tab + repr(op)
            operands_str += ","
        operands_str += "\n" + tabs + "]" 

        return f'{tabs}Expression(operation="{self._operation}", operands={operands_str})'

    def __str__(self) -> str:
        op_count = self._operation._operand_count
        if op_count == 1: 
            return f"({self._operation} {self._operands[0]})"
        elif op_count == 2:
            return f"({self._operands[0]} {self._operation} {self._operands[1]})"
        else:
            operands = ", ".join(self._operands)
            return f"[{self._operation}]({operands})"

