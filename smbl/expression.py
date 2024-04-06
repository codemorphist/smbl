from .var import Var
from .domain import Domain, DefaultDomain
from .operation_handler import OperationHandler
from .operation import Operation
from .function import Function


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
                new_operands.append(op(**kwargs))
            else:
                raise Exception(f"{type(op)} not valid type for calculate Expression")

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
