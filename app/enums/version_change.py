from enum import Enum


class VersionChangeType(str, Enum):

    CREATE = "CREATE"

    UPDATE = "UPDATE"

    RESTORE = "RESTORE"

    IMPORT = "IMPORT"