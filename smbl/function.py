from .var import Var, Constant, Expression
from .operation import *
from typing import Callable


class Function(Expression): 
    def __init__(self,
                 vars: set[Var], 
                 func: Callable[[float], float],
                 deriv: Callable[[float], float] = None):
        """
        :param symbol: symbol or name of funtion
        :param vars: set of vars in function
        :param func: callback for function 
        :param deriv: callback for function derivative
        """
        self._vars = vars 
        self._func = func
        self._deriv = deriv
    
    @property
    def symbol(self):
        return self._symbol

    def derivative(self):
        if self._deriv is not None:
            return self._deriv
        else:
            return D(self._func)

    @property
    def d(self):
        return self.derivative()

    def __str__(self) -> str:
        vars = ", ".join([v.name for v in self._vars])
        return f"{self._func}"

    def __repr__(self, ident: int=0) -> str:
        pass


def D(func) -> Function:
    if isinstance(func, Constant):
        return Function(
            vars=set(),
            func=Constant(0)
        )
    elif isinstance(func, Var):
        return Function(
            vars=set(),
            func=Constant(1)
        )
    elif isinstance(func, Function):
        if func._deriv is not None:
            return func._deriv
        else:
            return D(func._func)
    elif isinstance(func, Expression):
        op = func._operation
        if op not in [Add, Sub, Mul, Div, Pow]:
            raise TypeError(f"Invalid operation `{op}` to take derivative")

        f, g = func._operands
        print(f, g)
        if op is Add:
            return function(D(f)  + D(g))
        elif op is Sub:
            return function(D(f) - D(g))
        elif op is Mul:
            return function(D(f)*g + f*D(g))
        elif op is Div:
            return function((D(f)*g - f*D(g))/(g**2))
        else:
            return function(f ** g * (D(g) * Ln(f) + g*D(Ln(f)))) 
    else:
        raise TypeError(f"Invalid type to take derivative `{type(func)}`")


def function(other) -> Function:
    """
    Convert Var, Constant, or Expression to Function
    """
    if type(other) in [Var, Constant, Expression]:
        return Function(
            vars=other.vars,
            func=other
        )
    elif isinstance(other, Function):
        return other
    else:
        raise TypeError(f"Can't convert `{type(other)}` to Function")


# --- BASIC MATH FUNCTIONS ---

class Ln(Function):
    def __init__(self, param: Var | Expression | Function):
        self._param = param
        self._vars = param.vars 
        self._func = self.__ln__
        self._deriv = 1 / param * D(param)

    def __ln__(self, **kwargs):
        pass

    def __str__(self) -> str:
        return f"ln({self._param})"

