from enum import Enum


class LockRequestStatus(str, Enum):

    WAITING = "waiting"

    NOTIFIED = "notified"

    ACCEPTED = "accepted"

    REFUSED = "refused"

    EXPIRED = "expired"