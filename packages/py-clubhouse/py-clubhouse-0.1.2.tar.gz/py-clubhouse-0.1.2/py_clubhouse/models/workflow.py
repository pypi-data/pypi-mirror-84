from typing import NoReturn, Any

from py_clubhouse import models
from .workflow_state import WorkflowState


class Workflow(models.ClubBASE):
    def __setattr__(self, attribute: str, value: Any) -> NoReturn:
        """Objectify states data attribute."""
        if attribute == "states":
            value = [WorkflowState(self._req, v) for v in value]

        super().__setattr__(attribute, value)
