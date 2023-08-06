from __future__ import annotations


class Xref:
    """
    A database cross-reference to a soecific ID in a specific target database.
    """

    def __init__(self, target_db: str, target_id: str):
        self.target_db = target_db
        self.target_id = target_id
