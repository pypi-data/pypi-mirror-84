from typing import Dict
import logging
import requests

from ..const import ENDPOINT_HOST, ENDPOINT_PATH


logger = logging.getLogger(__name__)


class RequestAPI:
    def __init__(self, api_token, user_agent=None):
        self._headers = {"Content-Type": "application/json", "Clubhouse-Token": api_token, "User-Agent": "agent/007"}

    def call(self, method: str, path: str, **kwargs: int) -> Dict:
        """http request to call
        :param method:                  HTTP method
        :param path:                    url path to call
        :param kwargs:                  extra data
        :return:                        json response, empty dict otherwise
        """
        if not path.startswith(ENDPOINT_PATH):
            path = f"{ENDPOINT_PATH}/{path}"

        url = f"{ENDPOINT_HOST}{path}"
        req_to_call = getattr(requests, method)
        kwargs.update({"headers": self._headers.copy()})

        try:
            req = req_to_call(url, **kwargs)
            req.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logger.error(str(http_err), exc_info=True)
        except Exception as err:
            logger.error(f"Other error occurred when making request: {err}.", exc_info=True)
        else:
            return req.json()

        return dict()
