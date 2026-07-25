"""
Audit action enumeration.
"""

from enum import Enum


class AuditAction(str, Enum):
    """
    Represents actions recorded in the audit log.
    """

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    VALIDATE = "validate"
    REJECT = "reject"
    PUBLISH = "publish"
    IMPORT = "import"
    EXPORT = "export"
    LOCK = "lock"
    UNLOCK = "unlock"