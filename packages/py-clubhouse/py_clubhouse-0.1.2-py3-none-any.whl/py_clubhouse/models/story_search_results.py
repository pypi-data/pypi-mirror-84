from .base import ClubBASE


class StorySearchResults(ClubBASE):
    STR_FIELD = "total"

    def get_next(self):
        data = self._req.call("get", self.next)
        return StorySearchResults(self._req, data)
