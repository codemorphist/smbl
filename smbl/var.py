from .domain import Domain, DefaultDomain
from .operation_handler import OperationHandler
from .operation import Operation


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
        return cls.get_var(attr)


class Var(OperationHandler, metaclass=VarMeta):
    """
    Variable class

    __new__: Create new varible and save it in storage of all variables
    __defined_vars__: dict[str, Var] Dict with every variable by name
    """

    __defined_vars__ = {}

    def __new__(cls, name, value: any=None, domain: Domain=DefaultDomain()):
        if name not in cls.__defined_vars__:
            self = super().__new__(cls)
            self._name = name
            
            if value is not None and not value in domain():
                raise ValueError(f"({value}) not in {domain.__name__}")

            self._value = value
            self._domain = domain

            cls.__defined_vars__[name] = self
        else:
            raise NameError(f"Variable with name ({name}) alredy exist")
        return cls.__defined_vars__[name]

    @classmethod
    def get_var(cls, name: str):
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

    def __call__(self) -> any:
        return self.value

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def value(self) -> any:
        return self._value
    @value.setter
    def value(self, val: any):
        if val in self._domain:
            self._value = val
        else:
            raise ValueError(f"({val}) not in {self.domain}")

    @property
    def domain(self):
        return self._domain
    
    def __repr__(self) -> str:
        return f'Var("{self.name}", value={self.value}, domain={self.domain})'

    def __str__(self) -> str:
        return self.name

    def __hash__(self): 
        return hash(self._name)

