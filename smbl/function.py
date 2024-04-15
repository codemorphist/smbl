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
        return f"func({vars})"

    def __repr__(self, ident: int=0) -> str:
        pass


def D(func):
    return f"derivative of {f}"


def function(other) -> Function:
    """
    Convert Var, Constant, or Expression to Function
    """
    if type(other) in [Var, Constant, Expression]:
        return Function(
            vars=other.vars,
            func=other
        )
    else:
        raise TypeError(f"Can't convert `{type(other)}` to Function")


# --- BASIC MATH FUNCTIONS ---

class Ln(Function):
    def __init__(self, param: Var | Expression | Function):
        self._symbol = "ln"
        self._vars = param.vars 
        self._func = self.__ln__
        self._deriv = 1 / param * param.d

    def __ln__(self, **kwargs):
        pass

