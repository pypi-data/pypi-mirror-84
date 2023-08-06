from __future__ import annotations


class Zstate:

    def __init__(self, zstate: str = None):
        self.zstate = zstate
        self._input = None

    def __str__(self) -> str:
        return self.zstate

    @classmethod
    def parse(cls, string) -> Zstate:
        zstate = cls(string.strip())
        zstate._input = string
        return zstate
