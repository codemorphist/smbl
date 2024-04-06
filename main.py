from smbl import Var, Expression
from smbl.domain import PrimeDomain, NaturalDomain
from smbl.function import Function

x = Var("x", domain=NaturalDomain())
y = Var("y", domain=PrimeDomain())
z = Var("z")


f1 = Function("f1", (x, y, z), x + y + z)
e = Var.x + (y * f1 / (f1 - z))
print(repr(e))
