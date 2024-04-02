# SMBL

**SMBL** — is simple package written on Python for symbolic calculations

## Features
- `Var()` — You can create variables and use it in Expressions
- `Domain()` — You can create some rule for variables
- `Expression()` — You can create Expression from Constants(int, float, complex) or from variables, using operation to operate by it
- `Operation()` — You can create operation to operate by variables
- ~~`Function()`~~ —  **TODO**

## Navigation:
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Imports](#imports)
   * [Default](#default)
   * [Implement own classes](#implement-own-classes)
- [Variable](#variable)
   * [Usage](#usage)
- [Expression](#expression)
   * [Usage](#usage-1)
   * [Calculation](#calculation)
- [Domain usage and default domains](#domain-usage-and-default-domains)
   * [Usage](#usage-2)
   * [Own Domain](#own-domain)
   * [Examples](#examples)
- [Operation ](#operation)
   * [Usage](#usage-3)
   * [Own Operation](#own-operation)
   * [Examples](#examples-1)

<!-- TOC end -->

## Imports

### Default

 Imports what you need to work with **SMBL**

```python
from smbl import Var    # For create new variables
from smbl.domain import *   # For use default domains
```

### Implement own classes
Imports if you want to expand functionality of some classes or want to create your own based on exist class to use it for your special calculations

```python
from smbl.domain import Domain  # For implement you own domain class
from smbl.operation import Operation    # For implement you own operation
# from smbl.function import Function # For Implement you own Function
```
Implementations example:
- [Domain](#own-domain)
- [Operator](#own-operation)

## Variable

### Usage

This section demonstrates how to create and use variables

```python 
>>> Var(some_name, value=some_value, domain=some_domain)
>>> Var.some_name		# you can acces to variable without save it to python variable
    Var(name="some_name", value="some_value", domain=some_domain)
>>> Var.some_name.value = some_new_value
```

## Expression

### Usage

This section demonstrates how to create Expressions from variables

> **_NOTE:_** You can also use other Expressions for variables values

```python 
>>> Var("x")
    Var("x", value=None, domain=DefaultDomain)
>>> Var("y")
    Var("y", value=None, domain=DefaultDomain)
>>> e = Var.x + Var.y
>>> e
    Expression(operation="+", operands=[
        Var("x", value=None, domain=DefaultDomain),
        Var("y", value=None, domain=DefaultDomain),
    ])
>>> str(e)
    '(x + y)'
```

### Calculation

This section demonstrates how to calculate expression, with given variables values

> **_NOTE:_** You can also use other Expressions for variables values

```python
>>> Var("x")
    Var("x", value=None, domain=DefaultDomain)
>>> Var("y")
    Var("y", value=None, domain=DefaultDomain)
>>> e = Var.x + Var.y
>>> e(x=4, y=5)
    9
>>> e2 = e(y=5)
>>> str(e2)
    '(x + 5)'
```

## Domain usage and default domains

This section demonstrates how use domains

> **_NOTE:_** Domain it is something like rule for you variables, for examples you can create variable the values of which can only be prime numbers 

### Usage

This section demonstrates how to check value in Domain

```python
some_value in TestDomain()		# return True if some_value in TestDomain else False
```

### Own Domain

If you want to create your own domain you should create a class that inherits from `Domain` and override the `__in_domain__` method:

```python
from smbl.domain import Domain

class OwnDomain(Domain):
    def __in_domain__(self, value: any) -> bool:
        """
        Write code to check value in domain
        """
        pass
```

### Examples
```python

class DefaultDomain(Domain):
    """
    Default domain which alway return True
    """
    def __in_domain__(self, param: any) -> bool:
        return True


class EvenDomain(Domain):
    """
    Domain for even numbers
    """
    def __in_domain__(self, value: int) -> bool:
        return value % 2 == 0


class OddDomain(Domain):
    """
    Domain for odd numbers
    """
    def __in_domain__(self, value: int) -> bool:
        return not value in EvenDomain()


class IntegerDomain(Domain):
    """
    Domain for integer numbers

    ..., -3, -2, -1, 0, 1, 2, 3, ...
    """
    def __in_domain__(self, value: int) -> bool:
        return isinstance(value, int)


class NaturalDomain(Domain):
    """
    Domain for natural numbers

    0, 1, 2, 3, 4, 5, 6, 7, 8, ...
    """
    def __in_domain__(self, value: int) -> bool:
        return value in IntegerDomain() and value >= 0


class PrimeDomain(Domain):
    """
    Domain for only positive prime numbers

    2, 3, 5, 7, 11, 13, 17, ...
    """
    def __is_prime__(value: int) -> bool:
        """
        Check natural number is prime
        """
        if value < 2:
            return False
        if value == 2: 
            return True

        if value in EvenDomain():
            return False
        
        i = 3 
        while i*i <= value:
            if value % i:
                return False
            i += 2
        return True

    def __in_domain__(self, value: int) -> bool:
        return value in NaturalDomain() and cls.__is_prime__(value)


class IntegerPrimeDomain(Domain):
    """
    Domain for positive and negative prime numbers

    ..., -17, -13, ..., -2, 2, 3, 5, 7, 11, 13, 17, ...
    """
    def __in_domain__(self, value: int) -> bool:
        return value in IntegerDomain() and abs(value) in PrimeDomain()


class RealDomain(Domain):
    """
    Domain for real numbers

    0.(3), sqrt(2)/2, 0, 1, -pi, e, ...
    """
    def __in_domain__(self, value: float | int) -> bool:
        return isinstance(value, float) or value in IntegerDomain()


class ComplexDomain(Domain):
    """
    Domain for complex numbers

    1+i, i, 0, 1, 14+8i, ...
    """
    def __in_domain__(self, value: float | int | complex):
        return value in RealDomain() or isinstance(value, complex)
```

## Operation 

This section demonstrates how to use operation

> **_NOTE:_** Operators is function what take some arguments and calculate result of this arguments

### Usage

This section demonstrates how to calculate value using operation

```python
res = TestOperator(val1, val2,..., valn)
```

### Own Operation

You can create `UnaryOperation` and `BinaryOperation`:
```python
NewBinaryOperation = BinaryOperation("symbol", callback)
NewUnaryOperation = UnaryOperation("symbol", callback)
```

Also, you can implement operation with custom variables count:

```python
# One 
ThreeValueOperation = Operation("symbol", callback, operand_count=3)

# Two
class ThreeValueOperation(Operation):
    def __init__(self,
                 symbol: str,
                 operation: callable):
        super().__init__(symbol, operation, operand_count=3)

```

### Examples

```python
Add = BinaryOperation("+", lambda a, b: a + b)
Sub = BinaryOperation("-", lambda a, b: a - b)
Mul = BinaryOperation("*", lambda a, b: a * b)
Div = BinaryOperation("/", lambda a, b: a / b)
TrueDiv = BinaryOperation("//", lambda a, b: a // b)
Mod = BinaryOperation("%", lambda a, b: a % b)
Pow = BinaryOperation("^", lambda a, b: a**b)
```

