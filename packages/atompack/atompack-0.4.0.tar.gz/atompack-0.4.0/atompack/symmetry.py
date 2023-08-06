"""An abstraction for crystallographic spacegroups."""

import json
from typing import List, Union

import pkg_resources

SPACEGROUPS = None


def _load_spacegroups():
    global SPACEGROUPS
    if SPACEGROUPS is None:
        SPACEGROUPS = json.load(pkg_resources.resource_stream(__name__, "data/spacegroups.json"))
    return SPACEGROUPS


class Spacegroup(object):
    """Representation of a spacegroup.

    Args:
        spg: Hermann Mauguin symbol or International spacegroup number.
    """

    def __init__(self, spg: Union[int, str]) -> None:
        spgs = _load_spacegroups()
        group = None
        if type(spg) is int:
            if spg > 230 or spg < 1:  # type: ignore
                raise ValueError("`spg` must be in range 1..230")
            group = spgs[spg - 1]  # type: ignore
        elif type(spg) is str:
            for i, _group in enumerate(spgs):
                if _group["hermann_mauguin"] == spg:
                    group = spgs[i]
                    break
            if group is None:
                raise ValueError("`spg` is not a valid Hermann Mauguin spacegroup symbol")
        else:
            raise TypeError("`spg` must be of type int or str")

        self._bravais_lattice = group["bravais_lattice"]
        self._international_number = group["international_number"]
        self._hermann_mauguin = group["hermann_mauguin"]
        self._genpos = group["genpos"]

    ####################
    #    Properties    #
    ####################

    @property
    def bravais_lattice(self) -> str:
        """Returns the bravais lattice name."""
        return self._bravais_lattice

    @property
    def international_number(self) -> int:
        """Returns the international spacegroup number."""
        return self._international_number

    @property
    def hermann_mauguin(self) -> str:
        """Returns the Hermann Mauguin spacegroup symbol."""
        return self._hermann_mauguin

    @property
    def genpos(self) -> List[str]:
        """Returns the general position expressions."""
        return self._genpos

    #########################
    #    Special Methods    #
    #########################

    def __eq__(self, other) -> bool:
        if not isinstance(other, Spacegroup):
            return NotImplemented
        return self.international_number == other.international_number
