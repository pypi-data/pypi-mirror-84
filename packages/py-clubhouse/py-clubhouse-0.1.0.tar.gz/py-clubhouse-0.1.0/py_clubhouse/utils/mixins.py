import os
from typing import Dict
import logging
import requests

from ..const import ENDPOINT_HOST, ENDPOINT_PATH


logger = logging.getLogger(__name__)
API_BASE = f"{ENDPOINT_HOST}{ENDPOINT_PATH}"


class RequestsMixin:
    """for making external api requests"""

    def _request(self, method: str, *args, **kwargs: int) -> Dict:
        req_to_call = getattr(requests, method)
        base = os.path.join(API_BASE, *[str(s).strip("/") for s in args])
        url = f"{base}?token={self.api_key}"

        try:
            req = req_to_call(url, **kwargs)
            req.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logger.error(str(http_err))
        except Exception as err:
            logger.error(f"Other error occurred when making request: {err}.")
        else:
            return req.json()

        return dict()
