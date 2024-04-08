from smbl import Var
from smbl import Function
from smbl.domain import PrimeDomain, NaturalDomain

x = Var("x", domain=NaturalDomain())
y = Var("y", domain=PrimeDomain())
z = Var("z")

e = x + y
print(e(x=1))


f1 = Function("f1", [x, y], x + y)
f2 = Function("f2", [z, ], z)

f3 = f1 + f2

print(f3(x=1, y=1, z=2))
print(f2(z=1))

