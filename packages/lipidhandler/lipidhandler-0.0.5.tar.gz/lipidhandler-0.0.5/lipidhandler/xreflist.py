from __future__ import annotations

from typing import List

from lipidhandler.xref import Xref


class XrefList:

    def __init__(self, xreflist: List[Xref] = None):
        if xreflist:
            self.xreflist = xreflist
        else:
            self.xreflist = []

    def __len__(self):
        return len(self.xreflist)

    def __getitem__(self, item):
        return self.xreflist[item]

    def __iter__(self):
        return iter(self.xreflist)

    def append(self, item) -> None:
        if isinstance(item, Xref):
            self.xreflist.append(item)
        else:
            raise TypeError('Not of type Xref')
