from smbl import Var, Expression
import math

x = Var("x")
y = Var("y")
z = Var("z")

e1 = 2 * x
e2 = x + 1
e = e2**e1

print(e.derivative(x))
