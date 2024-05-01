from smbl.domain import DefaultDomain
from smbl.domain import OddDomain, EvenDomain
from smbl.domain import PrimeDomain, IntegerPrimeDomain


def test_default_domain():
    assert 5 in DefaultDomain(), "Invalid DefaultDomain result for int"
    assert 1.0 in DefaultDomain(), "Invalid DefaultDomain result for float"
    assert (1+1j) in DefaultDomain(), "Invalid DefaultDomain result for complex"


def test_odd_even_domains():
    # OddDomain
    assert 3 in OddDomain(), "3 is Odd Number"
    assert 5 in OddDomain(), "5 is Odd Number"
    assert 2 not in OddDomain(), "2 is not Odd Number"
    assert 1.0 not in OddDomain(), "1.0 is not Odd Number"

    # EvenDomain
    assert 2 in EvenDomain(), "2 is Even Number"
    assert 6 in EvenDomain(), "6 is Even Number"
    assert 3 not in EvenDomain(), "3 is not Even Number"
    assert 2.0 not in EvenDomain(), "1.0 is not Even Number"


def test_prime_domain():
    assert 2 in PrimeDomain(), "2 is Prime Number"
    assert 1 not in PrimeDomain(), "1 is not Prime Number"
    assert 0 not in PrimeDomain(), "0 is not Prime Number"
    assert 3301 in PrimeDomain(), "3301 is Prime Number"


def test_integer_prime_domain():
    assert -2 in IntegerPrimeDomain(), "-2 is Integer Prime Number"
    assert -1 not in IntegerPrimeDomain(), "-1 is not Integer Prime Number"
    assert 0 not in IntegerPrimeDomain(), "0 is not Integer Prime Number"
    assert -3301 in IntegerPrimeDomain(), "-3301 is Integer Prime Number"

