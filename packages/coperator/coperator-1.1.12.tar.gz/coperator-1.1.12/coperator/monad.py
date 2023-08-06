from typing import Any


def monad(bfn: Any) -> Any:
    """monad.

    :param bfn:
    :type bfn: Any
    :rtype: Any
    """

    def bind(fn: Any) -> Any:
        """bind.

        :param fn:
        :type fn: Any
        :rtype: Any
        """
        try:
            if fn is None:
                return bfn
            elif bfn is None:
                return monad(None)
            else:
                return monad(fn(bfn))
        except:  # noqa: E722
            return monad(None)

    return bind
