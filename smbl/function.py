from .var import Var, Constant, Expression
from typing import Callable


class Function(Expression): 
    def __init__(self,
                 vars: set[Var], 
                 func: Callable[[float], float],
                 deriv: Callable[[float], float]):
        """
        :param vars: set of vars in function
        :param func: callback for function 
        :param deriv: callback for function derivative
        """
        self._vars = vars 
        self._func = func
        self._deriv = deriv
    
    def derivative(self):
        func = self._func
        if isinstance(func, Constant):
            return Function(vars=set(), func=func)

    @property
    def d(self):
        return self.derivative()

    def __str__(self) -> str:
        pass

    def __repr__(self, ident: int=0) -> str:
        pass
