from .operation import Add, Sub, Mul, Div, FloorDiv, Mod, Pow


class OperationHandler:
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

    def __rmod__(self, other):
        return Expression(Mod, other, self)

    def __rpow__(self, other):
        return Expression(Pow, other, self)
