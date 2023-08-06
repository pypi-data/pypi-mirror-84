from typing import Dict

from ..utils.request import RequestAPI


class Workflow:
    STR_FIELD = "id"

    def __init__(self, req: RequestAPI, data: Dict) -> None:
        self._req = req
        self.__dict__.update(**data)

    def __repr__(self) -> str:
        """Return an object initialization representation of the instance."""
        return f"{self.__class__.__name__}({self.STR_FIELD}={str(self)!r})"

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        return str(getattr(self, self.STR_FIELD))
