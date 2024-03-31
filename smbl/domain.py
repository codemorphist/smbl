class Domain:
    def __in_domain__(cls, param: any) -> bool:
        """
        Method which check value in Domain
        """
        pass

    def __repr__(self) -> str:
        return self.__name__

    def __str__(self) -> str:
        return repr(self)

    def __new__(cls, param: any=None) -> bool:
        return cls.__in_domain__(cls, param)


# --- DEFAULT DOMAINS ---

class DefaultDomain(Domain):
    """
    Default domain which alway return True
    """
    def __in_domain__(cls, param: any) -> bool:
        return True


class EvenDomain(Domain):
    """
    Domain for even numbers
    """
    def __in_domain__(cls, value: int) -> bool:
        return value % 2 == 0


class OddDomain(Domain):
    """
    Domain for odd numbers
    """
    def __in_domain__(cls, value: int) -> bool:
        return not EvenDomain(value)


class IntegerDomain(Domain):
    """
    Domain for integer numbers

    ..., -3, -2, -1, 0, 1, 2, 3, ...
    """
    def __in_domain__(cls, value: int) -> bool:
        return isinstance(value, int)


class NaturalDomain(Domain):
    """
    Domain for natural numbers

    0, 1, 2, 3, 4, 5, 6, 7, 8, ...
    """
    def __in_domain__(cls, value: int) -> bool:
        return IntegerDomain(value) and value >= 0


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

        if EvenDomain(value):
            return False
        
        i = 3 
        while i*i <= value:
            if value % i:
                return False
            i += 2
        return True

    def __in_domain__(cls, value: int) -> bool:
        return NaturalDomain(value) and cls.__is_prime__(value)


class IntegerPrimeDomain(Domain):
    """
    Domain for positive and negative prime numbers

    ..., -17, -13, ..., -2, 2, 3, 5, 7, 11, 13, 17, ...
    """
    def __in_domain__(cls, value: int) -> bool:
        return IntegerDomain(value) and PrimeDomain(abs(value))


class RealDomain(Domain):
    """
    Domain for real numbers

    0.(3), sqrt(2)/2, 0, 1, -pi, e, ...
    """
    def __in_domain__(cls, value: float | int) -> bool:
        return isinstance(value, float) or IntegerDomain(value)


class ComplexDomain(Domain):
    """
    Domain for complex numbers

    1+i, i, 0, 1, 14+8i, ...
    """
    def __in_domain__(cls, value: float | int | complex):
        return RealDomain(value) or isinstance(value, complex)

# --- DEFAULT DOMAINS ---
