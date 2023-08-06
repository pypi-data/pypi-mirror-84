from coperator.myoperator import factory_operator


class Example:
    """Example."""

    def __init__(self, x: int) -> None:
        """__init__.

        :param x:
        :type x: int
        :rtype: None
        """
        self._x: int = self.set_x(x)

    def set_x(self, x: int) -> int:
        """set_x.

        :param x:
        :type x: int
        :rtype: int
        """
        return x

    def get_x(self) -> int:
        """get_x.

        :rtype: int
        """
        return self._x

    def __str__(self) -> str:
        """__str__.

        :rtype: str
        """
        return str(self.get_x())


@factory_operator(Example, Example, Example)
def op(A: Example, B: Example) -> Example:
    """op.

    :param A:
    :type A: Example
    :param B:
    :type B: Example
    :rtype: Example
    """
    return Example(A.get_x() + B.get_x())


E1: Example = Example(1)
E2: Example = Example(2)
E3: Example = Example(3)

print(E1 * op * E2 * op * E3)
