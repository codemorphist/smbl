from .domain import Domain, DefaultDomain
from .operation import Operation
from .operation import (Add, Sub, Mul, Div, 
                        FloorDiv, Mod, Pow)

from typing import TypeAlias


Constant = int | float | complex


class OperationHandler:
    """
    Default operations for Var, Expression and Function
    """
    def __add__(self, other): 
        return Expression(Add, self, other)

    def __sub__(self, other): 
        return Expression(Sub, self, other)

    def __mul__(self, other): 
        return Expression(Mul, self, other)

    def __truediv__(self, other): 
        return Expression(Div, self, other)

    def __floordiv__(self, other):
        return Expression(FloorDiv, self, other)

    def __mod__(self, other):
        return Expression(Mod, self, other)

    def __pow__(self, other):
        return Expression(Pow, self, other)

    def __radd__(self, other): 
        return Expression(Add, other, self)

    def __rsub__(self, other): 
        return Expression(Sub, other, self)

    def __rmul__(self, other): 
        return Expression(Mul, other, self)

    def __rtruediv__(self, other): 
        return Expression(Div, other, self)

    def __rfloordiv__(self, other):
        return Expression(FloorDiv, other, self)


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
            
            if value is not None and not value in domain():
                raise ValueError(f"({value}) not in {domain.__name__}")

            self._value = value
            self._domain = domain

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
            raise Exception(f"Variable with name ({name}) doesn't exist")

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


class Expression(OperationHandler):
    def __init__(self, 
                 operation: Operation, 
                 *operands: list[any]):
        self._operation = operation

        if len(operands) > operation._operand_count:
            raise Exception("Too many operands for operation")
        elif len(operands) < operation._operand_count:
            raise Exception("Not enought operands for operation")
        else:
            self._operands = operands

    def __call__(self, **kwargs):
        """
        Calculate value of Expression or return new 
        Expression with replace given Vars values 
        to Constants
        
        If some Vars value not given return Expression,
        where Var with given values was replaced by 
        constant
        """
        for var, value in kwargs.items():
            var = getattr(Var, var)
            var.value = value

        new_operands = []
        for op in self._operands:
            if isinstance(op, Constant):
                new_operands.append(op)
            elif isinstance(op, Var):
                if op.value is None:
                    new_operands.append(op)
                else:
                    new_operands.append(op.value)
            elif isinstance(op, Expression):
                # If Expression calculate value recursively
                new_operands.append(op(**kwargs))
            else:
                raise TypeError(f"{type(op)} not valid type for calculate Expression")

        return self._operation(*new_operands)
   
    def __repr__(self, ident: int=0) -> str:
        tab = "  "
        tabs = tab * ident
        operands_str = f"["
        for op in self._operands:
            operands_str += "\n"
            if isinstance(op, Expression) or isinstance(op, Function):
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


class Function(Expression):        
    def __init__(self, 
                 name: str, 
                 variables: set[Var],
                 callback: callable):
        """
        :param name: name of function, in lower case
        :param variables: set of variables which using in function
        :param callback: callable object which calculate function result
        """
        self._name = name.lower().strip()
        self._variables = set(variables)
        self._callback = callback
        self._params_count = len(self._variables)

    @property
    def name(self) -> str:
        return self._name

    def __call__(self, **values) -> any:
        if len(self._variables) > self._params_count:
            raise Exception(f"Too many argument for function ({self.name}), must be {self._params_count}")
        for var, value in values.items():
            var = getattr(Var, var)
            if var not in self._variables:
                raise NameError(f"Invalid variable name: `{var}` in function ({self.name})")

        return self._callback(**values)

    def __repr__(self, ident=0) -> str:
        tab = "  "
        tabs = tab * ident
        vars_str = "[" + f"\n{tabs}{tab}".join([""] + [repr(var) for var in self._variables]) + f"\n{tabs}]"
        return f"{tabs}Function(name={self.name}, variables={vars_str})"

    def __str__(self) -> str:
        vars = ", ".join([str(var) for var in self._variables])
        return f"{self._name}({vars})"
