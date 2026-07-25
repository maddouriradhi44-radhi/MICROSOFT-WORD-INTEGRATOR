from enum import Enum

class Versionstatus(str, Enum):
    """Possible validation states for a version."""

    ATTENTE = "attente"
    ACCEPTEE = "acceptee"
    REFUSEE = "refusee"
    