from smbl import Var, Expression
from smbl.domain import PrimeDomain, NaturalDomain

x = Var("x")
y = Var("y")
z = Var("z")

e = x + y ** z + (34 - x)

print(repr(e))



