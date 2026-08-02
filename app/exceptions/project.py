"""
Project exceptions.

Custom exceptions related to project management.
"""


class ProjectNotFoundException(Exception):
    """
    Raised when a project cannot be found.
    """

    def __init__(self, project_id: int):
        super().__init__(
            f"Project with id {project_id} was not found."
        )