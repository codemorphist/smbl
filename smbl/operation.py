from typing import Any, Callable


class Operation:
    def __init__(self, symbol: str, operation: Callable, operand_count: int = 2):
        """
        :param symbol: symbol of Operation
        :param operation: python function to calculate operation from
                          int, float or complex (or other)
        :param operand_count: operands for operation
        """
        self._symbol = symbol
        self._operation = operation
        self._operand_count = operand_count

    def __call__(self, *operands) -> Any:
        if len(operands) < self._operand_count:
            raise Exception("Not enought operands for calculate result")
        elif len(operands) > self._operand_count:
            raise Exception("Too many operands")
        else:
            return self._operation(*operands)

    def __repr__(self) -> str:
        return f'{type(self).__name__}(symbol="{self._symbol}")'

    def __str__(self) -> str:
        return self._symbol


class UnaryOperation(Operation):
    def __init__(self, symbol: str, operation: Callable):
        super().__init__(symbol, operation, operand_count=1)


class BinaryOperation(Operation):
    def __init__(self, symbol: str, operation: Callable):
        super().__init__(symbol, operation, operand_count=2)


# --- DEFAULT OPERATIONS ---
OpVar = UnaryOperation("VAR", lambda a: a())
OpConst = UnaryOperation("CONST", lambda a: a())


# TODO: Make +,-,*,/,//,%,^ operation classes

Add = BinaryOperation("+", lambda a, b: a + b)
Sub = BinaryOperation("-", lambda a, b: a - b)
Mul = BinaryOperation("*", lambda a, b: a * b)
Div = BinaryOperation("/", lambda a, b: a / b)
FloorDiv = BinaryOperation("//", lambda a, b: a // b)
Mod = BinaryOperation("%", lambda a, b: a % b)
Pow = BinaryOperation("^", lambda a, b: a**b)
# --- DEFAULT OPERATIONS ---
