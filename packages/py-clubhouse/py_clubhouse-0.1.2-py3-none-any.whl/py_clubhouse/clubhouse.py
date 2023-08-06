import logging
from typing import List

from py_clubhouse import models
from .endpoints import API_URLS
from .core.request import RequestAPI


logger = logging.getLogger(__name__)


class Clubhouse:
    def __init__(self, api_key) -> None:
        self._req = RequestAPI(api_key)

    def search_stories(self, query: str) -> List[models.Story]:
        """search stories by text.

        see https://help.clubhouse.io/hc/en-us/articles/360000046646-Search-Operators

        :param query:
        :return:                        list of Story(s)
        """
        assert isinstance(query, str), query
        kwargs = {"params": {"query": query}}
        data = self._req.call("get", API_URLS.get("search_stories"), **kwargs)
        results = models.StorySearchResults(self._req, data)
        items = results.data

        while results.next:
            results = results.get_next()
            items = [*items, *results.data]

        return [models.Story(self._req, d) for d in items]

    def get_story(self, story_id: int) -> models.Story:
        """get story by id
        :param story_id:
        :return:                        Story instance
        """
        assert isinstance(story_id, int), story_id
        data = self._req.call("get", f'{API_URLS.get("stories")}/{story_id}')
        return models.Story(self._req, data)

    def workflows(self) -> List[models.Workflow]:
        """get all workflows for a workspace
        :return:                        list of Workflow(s)
        """
        data = self._req.call("get", API_URLS.get("workflows"))
        return [models.Workflow(self._req, d) for d in data]
