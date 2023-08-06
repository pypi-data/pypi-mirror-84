import logging

from lipidhandler.lipidlist import LipidList
from lipidhandler.lipid import Lipid
from lipidhandler.xreflist import XrefList

log = logging.getLogger(__name__)


class ExternalApi:

    def __init__(self):
        pass

    @classmethod
    def search(cls, search_term) -> LipidList:
        """
        Use the external API to search for a term and return a LipidList.

        :param search_term: The Search term.
        :return: A LipidList
        """
        raise NotImplementedError

    @classmethod
    def get_xrefs(cls, lipid: Lipid) -> XrefList:
        """
        Takes a `Lipid` instance as input and searches for entities in the specified database.

        :param lipid: The input lipid.
        :return: The lipid with Xrefs.
        """
        raise NotImplementedError
