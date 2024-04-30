from smbl import Var, Constant, Expression
import math


def test_var_eq():
    x, y = Var.vars("x y")

    assert x == x, "Equal variables not equal"
    assert x == Var.x, "Equal variables not equal"

    assert x != y, "Not equal variables are equal"
    assert Var.x != Var.y, "Not equal variables are equal"

    del x
    del y


def test_const_eq():
    x = Var("x")
    x.value = 0

    assert Constant(0) == 0, "Constant(0) not equal 0"
    assert Constant(0.0) == 0.0, "Constant(0.0) not equal 0.0"
    assert Constant((1+1j)) == (1+1j), "Constant(1+1i) not equal 1+1i"
    assert Constant(0) == Constant(0), "Constant(0) not equal Constant(0)"
    assert Constant(0.0) == Constant(0.0), "Constant(0.0) not equal Constant(0.0)"
    assert Constant(1+1j) == Constant(1+1j), "Constant(1+1j) not equal Constant(1+1j)"
    assert Constant(0) == x(), "Constant(0) not equal to Var(name='x', value=0)"

    del x


def test_expr_eq():
    x, y = Var.vars("x y")
        
    ea = x + y
    es = x - y
    em = x * y
    ed = x / y

    assert ea == (x + y), "Assert Add equal error"
    assert ea == (x + y), "Assert Sub equal error"
    assert ea == (x + y), "Assert Mul equal error"
    assert ea == (x + y), "Assert Div equal error"

    
    ln = Expression.from_callable(math.cos, {x})

    e1 = x + ln
    e2 = x - ln
    e3 = x * ln
    e4 = x / ln
     
    assert e1 == (x + ln), "Assert Add equal error"
    assert e2 == (x - ln), "Assert Sub equal error"
    assert e3 == (x * ln), "Assert Mul equal error"
    assert e4 == (x / ln), "Assert Div equal error"

    del x
    del y

