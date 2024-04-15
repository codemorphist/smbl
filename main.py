from smbl import Var


x = Var("x")
y = Var("y")
z = Var("z")

e = x + 2
print(e)
print(repr(e))
print(e.vars)

