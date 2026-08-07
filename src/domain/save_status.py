from enum import StrEnum


class SaveStatus(StrEnum):
    """
    Result of saving a snapshot record.
    """

    INSERTED = "INSERTED"
    UPDATED = "UPDATED"
    UNCHANGED = "UNCHANGED"