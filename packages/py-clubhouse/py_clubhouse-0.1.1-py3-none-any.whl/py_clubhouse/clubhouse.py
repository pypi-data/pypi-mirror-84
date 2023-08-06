import logging
from typing import List

from .endpoints import API_URLS
from .models.story import Story
from .models.workflow import Workflow
from .utils.request import RequestAPI


logger = logging.getLogger(__name__)


class Clubhouse:
    def __init__(self, api_key, ignored_status_codes=None) -> None:
        self.ignored_status_codes = ignored_status_codes or []

        self._req = RequestAPI(api_key)

    def search_stories(self) -> List[Story]:
        kwargs = {"params": {"query": "state:Staging"}}
        result = self._req.call("get", API_URLS.get("search_stories"), **kwargs)
        items = result["data"]

        while "next" in result and result["next"]:
            result = self._req.call("get", result["next"])
            items = [*items, *result["data"]]
        return [Story(self._req, d) for d in items]

    def get_story(self, story_id: int) -> Story:
        data = self._req.call("get", f'{API_URLS.get("stories")}/{story_id}')
        return Story(self._req, data)

    def workflows(self) -> List[Workflow]:
        data = self._req.call("get", API_URLS.get("workflows"))
        return [Workflow(self._req, d) for d in data]
