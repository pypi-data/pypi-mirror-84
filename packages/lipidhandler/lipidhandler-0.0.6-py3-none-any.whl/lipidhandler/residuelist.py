from __future__ import annotations
import logging
from typing import List

from lipidhandler.residue import Residue
from lipidhandler.helper import remove_outside_brackets

log = logging.getLogger(__name__)


class ResidueList:

    def __init__(self, residues: List[Residue] = None):
        if residues:
            self.residues = residues
        else:
            self.residues = []

    def __len__(self):
        return len(self.residues)

    def __getitem__(self, item):
        return self.residues[item]

    def __iter__(self):
        return iter(self.residues)

    @property
    def total_carbon_atoms(self) -> int:
        """
        Sum of all carbon atoms in this ResidueList.

        Only count if there are residues, return None (not 0) if there are no residues.
        """
        carbon_atoms = None
        for residue in self.residues:
            if carbon_atoms is None:
                carbon_atoms = residue.carbon_atoms
            else:
                carbon_atoms += residue.carbon_atoms
        return carbon_atoms

    @property
    def total_double_bonds(self) -> int:
        """
        Sum of all double bonds in this ResidueList

        Only count if there are residues, return None (not 0) if there are no residues.
        """
        double_bonds = None
        for residue in self.residues:
            if double_bonds is None:
                double_bonds = residue.double_bonds
            else:
                double_bonds += residue.double_bonds
        return double_bonds

    @property
    def residuelist_string(self) -> str:
        """
        Return string of the residue.

        :return: String of the residue.
        """
        return '/'.join([r.residue_string for r in self.residues])

    def sum(self):
        """
        Return sum of carbon atoms and double bonds of all Residues in this ResidueList as a Residue.
        """
        return Residue(self.total_carbon_atoms, self.total_double_bonds)

    @classmethod
    def parse(cls, string: str) -> ResidueList:
        """
        Parse a string and return a list of Residues.

        :param string: Input string.
        :return: ResidueList instance.
        """
        string = string.strip()
        # remove brackets
        log.debug(f'Parse input: {string}')

        # if string.count('(') > 1 or string.count(')') > 1:
        #     raise NotImplementedError('alternative chains not implemented')
        string = remove_outside_brackets(string)

        # check for residue splitter
        splittable = False
        split_char = None

        if '/' in string:
            splittable = True
            split_char = '/'
        elif '_' in string:
            splittable = True
            split_char = '_'

        residues = []
        residue_string_list = string.split(split_char)

        for residue_string in residue_string_list:
            residues.append(
                Residue.parse(residue_string)
            )

        return cls(residues)


