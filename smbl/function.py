from .var import Var
from .operation import *
from .operation_handler import OperationHandler


class Function(OperationHandler):        
    def __init__(self, 
                 name: str, 
                 variables: set[Var],
                 callback: callable):
        """
        :param name: name of function, in lower case
        :param variables: set of variables which using in function
        :param callback: callable object which calculate function result
        """
        self._name = name.lower().strip()
        self._variables = set(variables)
        self._callback = callback
        self._params_count = len(self._variables)

    @property
    def name(self) -> str:
        return self._name

    def __call__(self, **values) -> any:
        if len(self._variables) > self._params_count:
            raise Exception(f"Too many argument for function ({self.name}), must be {self._params_count}")
        for var, value in values.items():
            var = getattr(Var, var)
            if var not in self._variables:
                raise NameError(f"Invalid variable name: `{var}` in function ({self.name})")

        return self._callback(**values)

    def __repr__(self, ident=0) -> str:
        tab = "  "
        tabs = tab * ident
        vars_str = "[" + f"\n{tabs}{tab}".join([""] + [repr(var) for var in self._variables]) + f"\n{tabs}]"
        return f"{tabs}Function(name={self.name}, variables={vars_str})"

    def __str__(self) -> str:
        vars = ", ".join([str(var) for var in self._variables])
        return f"{self._name}({vars})"
