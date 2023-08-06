from __future__ import annotations
from typing import List

from lipidhandler.helper import remove_outside_brackets
from lipidhandler.zstate import Zstate


class ZstateList:

    def __init__(self, zstate_list: List[Zstate] = None):
        if zstate_list:
            self.zstate_list = zstate_list
        else:
            self.zstate_list = []
        self._input = None

    def __len__(self):
        return len(self.zstate_list)

    def __getitem__(self, item):
        return self.zstate_list[item]

    def __iter__(self):
        return iter(self.zstate_list)

    @classmethod
    def parse(cls, string) -> ZstateList:
        string = remove_outside_brackets(string.strip())

        zstate_string_list = []
        for zstate_name in string.split(','):
            zstate_string_list.append(
                Zstate.parse(zstate_name)
            )

        zstatelist = cls(zstate_string_list)
        zstatelist._input = string
        return zstatelist
