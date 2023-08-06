import json
from typing import Dict, Any, NoReturn

from py_clubhouse import models
from ..endpoints import API_URLS


class Story(models.ClubBASE):
    def __repr__(self) -> str:
        """Return an object initialization representation of the instance."""
        return f"{self.__class__.__name__}({self.STR_FIELD}={str(self)!r}, name={self.name!r})"

    def __setattr__(self, attribute: str, value: Any) -> NoReturn:
        """Objectify:
            branches, comments, commits, external_tickets, files, labels,
            linked_files, pull_requests, stats, story_links, and tasks data attributes.

        :param attribute:
        :param value:
        """
        if attribute == "branches":
            value = [models.Branch(self._req, v) for v in value]
        elif attribute == "comments":
            value = [models.Comment(self._req, v) for v in value]
        elif attribute == "commits":
            value = [models.Commit(self._req, v) for v in value]
        elif attribute == "external_tickets":
            value = [models.ExternalTicket(self._req, v) for v in value]
        elif attribute == "files":
            value = [models.File(self._req, v) for v in value]
        elif attribute == "labels":
            value = [models.Label(self._req, v) for v in value]
        elif attribute == "linked_files":
            value = [models.LinkedFile(self._req, v) for v in value]
        elif attribute == "pull_requests":
            value = [models.PullRequest(self._req, v) for v in value]
        elif attribute == "stats":
            value = models.StoryStats(self._req, value)
        elif attribute == "story_links":
            value = [models.TypedStoryLink(self._req, v) for v in value]
        elif attribute == "tasks":
            value = [models.Task(self._req, v) for v in value]

        super().__setattr__(attribute, value)

    def update(self, data: Dict) -> bool:
        """update a Story

        :param data:                    payload to update with
        :return:                        True if successful, False otherwise
        """
        url = f'{API_URLS.get("stories")}/{self.id}'
        req_json = self._req.call("put", url, data=json.dumps(data))
        self._to_attributes(req_json)

        return req_json and True
