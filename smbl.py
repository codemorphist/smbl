from domain import Domain, DefaultDomain


class VarMeta(type):
    """
    Metaclass for syntax sugar of Var

    Example:
    >>> Var("x")        # create (register) new variable
        Var("x", value=None, domain=DefaultDomain)
    >>> Var.x           # get variable without saving pointer to this variable 
        Var("x", value=None, domain=DefaultDomain)
    """

    def __getattr__(cls, attr):
        var = cls.get_var(attr)
        return var


class Var(metaclass=VarMeta):
    """
    Variable class

    __new__: Create new varible and save it in storage of all variables
    __defined_vars__: dict[str, Var] Dict with every variable by name
    """

    __defined_vars__ = {}

    def __new__(cls, name, value: any=None, domain: Domain=DefaultDomain):
        if name not in cls.__defined_vars__:
            self = super().__new__(cls)
            self._name = name
            
            if value is not None and not domain(value):
                raise Exception(f"({value}) not in {domain.__name__}")

            self._value = value
            self._domain = domain

            cls.__defined_vars__[name] = self
        else:
            raise Exception(f"Variable with name ({name}) alredy exist")
        return cls.__defined_vars__[name]

    @classmethod
    def get_var(cls, name):
        """
        Return variable by name

        Usage example:
        >>> Var("x")
            Var("x", value=None, domain=DefaultDomain)
        >>> Var.get_var("x")        # by method get_var()
            Var("x", value=None, domain=DefaultDomain)
        >>> Var.x                   # syntax sugar by __getattr__ method
            Var("x", value=None, domain=DefaultDomain)
        >>> Var.x.value = 1
        >>> Var.x
            Var("x", value=1, domain=DefaultDomain)        
        """
        if name in cls.__defined_vars__:
            return cls.__defined_vars__[name]
        else:
            raise Exception(f"Variable with name ({name}) doesn't exist")

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> any:
        return self._value
    @value.setter
    def value(self, value: any):
        if self._domain(value):
            self._value = value
        else:
            raise Exception(f"({value}) not in {self.domain_name}")

    @property
    def domain(self):
        return self._domain

    @property
    def domain_name(self) -> Domain:
        return self._domain.__name__

    def __str__(self): 
        return self.name

    def __add__(self, other): 
        pass 

    def __sub__(self, other): 
        pass 

    def __mul__(self, other): 
        pass 

    def __truediv__(self, other): 
        pass 
   
    def __repr__(self) -> str:
        return f'Var("{self.name}", value={self.value}, domain={self.domain_name})'

    def __str__(self) -> str:
        return self.name
    
    def __hash__(self): 
        return hash(self._name)


class Expression:
    def __init__(self):
        ...


