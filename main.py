from smbl import Var
from domain import *

Var("x", value=4, domain=RealDomain)
print(repr(Var.x))
