from smbl import Var
from smbl.domain import PrimeDomain, NaturalDomain

x = Var("x")
y = Var("y")
z = Var("z")

e = x + y ** z + (34 - x)

print(e)
print(e(y=5, z=4))





