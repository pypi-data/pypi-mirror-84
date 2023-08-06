import requests
import logging

from lipidhandler.lipidlist import LipidList
from lipidhandler.lipid import Lipid
from lipidhandler.xref import Xref
from lipidhandler.externalapis.apimodel import ExternalApi

log = logging.getLogger(__name__)


class SwissLipids(ExternalApi):
    NAME = 'SwissLipids'
    BASE_URL = 'https://www.swisslipids.org/api/index.php'

    def __init__(self):
        super(SwissLipids, self).__init__()

    def lipid_from_id(self, swisslipidsid: str) -> Lipid:
        """
        Call API to get details for a SwissLipids ID.

        :param swisslipidsid: The SwissLipids ID.
        :return: Return a Lipid.
        """
        request_url = self.BASE_URL + f'/entity/{swisslipidsid.strip()}'
        log.debug(f'Call: {request_url}')

        result = requests.get(request_url).json()

        # get abbreviation
        for synonym in result['synonyms']:
            if synonym['type'] == 'abbreviation':
                abbreviation = synonym['name']

                lipid = Lipid.parse(abbreviation)
                lipid.add_xref(Xref(self.NAME, swisslipidsid))
                return lipid

    def search(self, search_term) -> LipidList:
        lipidlist = LipidList()

        request_url = self.BASE_URL + f'/search?term={search_term}'
        log.debug(f"Request URL: {request_url}")

        result = requests.get(request_url).json()

        for entity in result:
            swisslipidsid = entity['entity_id']
            lipidlist.append(
                self.lipid_from_id(swisslipidsid)
            )

        return lipidlist
