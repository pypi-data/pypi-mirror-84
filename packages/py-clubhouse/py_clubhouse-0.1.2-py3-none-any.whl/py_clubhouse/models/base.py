from typing import Dict

from ..core.request import RequestAPI


class ClubBASE:
    STR_FIELD = "id"

    def __init__(self, req: RequestAPI, data: Dict) -> None:
        self._req = req
        self._to_attributes(data)

    def __repr__(self) -> str:
        """Return an object initialization representation of the instance."""
        return f"{self.__class__.__name__}({self.STR_FIELD}={str(self)!r})"

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        return str(getattr(self, self.STR_FIELD))

    def _to_attributes(self, data: Dict):
        for k, v in data.items():
            setattr(self, k, v)
