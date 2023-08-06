import logging
from typing import Dict

from .utils.mixins import RequestsMixin


logger = logging.getLogger(__name__)


class Clubhouse(RequestsMixin):
    def __init__(self, api_key, ignored_status_codes=None) -> None:
        self.ignored_status_codes = ignored_status_codes or []
        self.api_key = api_key

    def get(self, *args, **kwargs) -> Dict:
        return self._request("get", *args, **kwargs)

    def post(self, *args, **kwargs) -> Dict:
        return self._request("post", *args, **kwargs)

    def put(self, *args, **kwargs) -> Dict:
        return self._request("put", *args, **kwargs)

    def delete(self, *args, **kwargs) -> Dict:
        return self._request("delete", *args, **kwargs)
