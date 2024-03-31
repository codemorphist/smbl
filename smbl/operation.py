class Operation:
    def __init__(self, 
                 symbol: str, 
                 operation: callable, 
                 operand_count: int=2):
        self._symbol = symbol
        self._operation = operation
        self._operand_count = operand_count

    def __call__(self, *operands) -> any:
        if len(operands) < self._operand_count:
            raise Exception(f"Not enought operands for calculate result")
        elif len(operands) > self._operand_count:
            raise Exception(f"Too many operands")
        else:
            return self._operation(*operands)

    def __str__(self) -> str:
        return self._symbol


class UnaryOperation(Operation):
    def __init__(self, 
                 symbol: str,
                 operation: callable):
        super().__init__(symbol, operation, operand_count=1)


class BinaryOperation(Operation):
    def __init__(self,
                 symbol: str,
                 operation: callable):
        super().__init__(symbol, operation, operand_count=2)


# --- DEFAULT OPERATIONS ---

Add = BinaryOperation("+", lambda a, b: a + b)
Sub = BinaryOperation("-", lambda a, b: a - b)
Mul = BinaryOperation("*", lambda a, b: a * b)
Div = BinaryOperation("/", lambda a, b: a / b)
TrueDiv = BinaryOperation("//", lambda a, b: a // b)
Mod = BinaryOperation("%", lambda a, b: a % b)

Pow = BinaryOperation("^", lambda a, b: a**b)

# --- DEFAULT OPERATIONS --- 