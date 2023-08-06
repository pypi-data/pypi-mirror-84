import requests
import logging

from lipidhandler.lipidlist import LipidList
from lipidhandler.lipid import Lipid
from lipidhandler.xref import Xref
from lipidhandler.xreflist import XrefList
from lipidhandler.externalapis.apimodel import ExternalApi

log = logging.getLogger(__name__)


class SwissLipids(ExternalApi):
    NAME = 'SwissLipids'
    BASE_URL = 'https://www.swisslipids.org/api/index.php'

    def __init__(self):
        super(SwissLipids, self).__init__()

    @classmethod
    def search(cls, search_term: str) -> LipidList:
        lipidlist = LipidList()

        search_result = cls.run_search(search_term)

        if search_result:
            for entity in search_result:
                swisslipidsid = entity['entity_id']
                lipidlist.append(
                    cls.lipid_from_id(swisslipidsid)
                )

        return lipidlist

    @classmethod
    def get_xrefs(cls, lipid: Lipid, summed: bool = False) -> XrefList:
        xreflist = XrefList()

        try:
            search_term = lipid.abbreviation(summed)
        except Exception as e:
            log.debug(f"No abbreviation for lipid: {lipid.lipidclass}, {lipid.residueslist}.")
            log.error(f"Failed with {e}")
            search_term = lipid.abbreviation()

        search_result = cls.run_search(search_term)
        # search result can be empyt
        if search_result:
            for entity in cls.run_search(lipid.abbreviation(summed)):
                xreflist.append(Xref(cls.NAME, entity['entity_id']))

        return xreflist

    @classmethod
    def lipid_from_id(cls, swisslipidsid: str) -> Lipid:
        """
        Call API to get details for a SwissLipids ID.

        :param swisslipidsid: The SwissLipids ID.
        :return: Return a Lipid.
        """
        request_url = cls.BASE_URL + f'/entity/{swisslipidsid.strip()}'
        log.debug(f'Call: {request_url}')

        result = requests.get(request_url).json()

        # get abbreviation
        for synonym in result['synonyms']:
            if synonym['type'] == 'abbreviation':
                abbreviation = synonym['name']

                lipid = Lipid.parse(abbreviation)
                lipid.add_xref(Xref(cls.NAME, swisslipidsid))
                return lipid

    @classmethod
    def run_search(cls, search_term: str) -> dict:
        """
        Run a search against the SwissLipids API and return JSON result.

        :param search_term: The search term.
        :return: Result as JSON
        """
        request_url = cls.BASE_URL + f'/search?term={search_term}'
        log.debug(f"Request URL: {request_url}")

        result = requests.get(request_url)
        if result:
            return result.json()
