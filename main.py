from smbl import Var
from domain import *
from operation import *

Plus = BinaryOperation("+", lambda x, y: x + y)

print(Plus(3, 4))
print(Plus)

