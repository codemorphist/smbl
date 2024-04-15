from smbl import Var


x = Var("x")
y = Var("y")
z = Var("z")

e = x + y + z + x
print(e)
print(repr(e))
print(e.vars)

