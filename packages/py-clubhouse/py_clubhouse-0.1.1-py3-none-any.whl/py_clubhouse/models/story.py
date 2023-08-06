import json
from typing import Dict

from ..endpoints import API_URLS
from ..utils.request import RequestAPI


class Story:
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

    def update(self, data: Dict) -> bool:
        url = f'{API_URLS.get("stories")}/{self.story_id}'
        req_json = self._req.call("put", url, data=json.dumps(data))
        self.__dict__.update(**req_json)

        return req_json and True
