"""The internal abstraction for a network of optionally bonded atoms."""

import json
from typing import List, Tuple

from retworkx import PyGraph

from atompack.atom import Atom
from atompack.bond import Bond


class Topology(object):
    """Internal abstraction for a collection of atoms and bonds.
    
    Note:
        End users should not construct Topology objects directly.
    """

    def __init__(self) -> None:
        self._graph = PyGraph()

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_json(cls, s: str) -> 'Topology':
        """Initializes from a JSON string."""
        data = json.loads(s)
        res = cls()
        # process atoms
        for atom in data["atoms"]:
            res._graph.add_node(Atom.from_json(json.dumps(atom)))
        # process bonds
        for bond in data["bonds"]:
            bond = Bond.from_json(json.dumps(bond))
            res._graph.add_edge(*bond.indices, edge=bond)
        return res

    ####################
    #    Properties    #
    ####################

    @property
    def atoms(self) -> List[Atom]:
        """Returns a list of all atoms in the topology."""
        return self._graph.nodes()

    @property
    def bonds(self) -> List[Bond]:
        """Returns a list of all bonds in the topology."""
        return self._graph.edges()

    ########################
    #    Public Methods    #
    ########################

    def insert_atoms(self, *atoms: Atom) -> List[int]:
        """Inserts one or more atoms and returns their indices."""
        return self._graph.add_nodes_from(atoms)

    def remove_atoms(self, *indices: int) -> List[Atom]:
        """Removes and returns one or more atoms."""
        res = [self._graph.get_node_data(index) for index in indices]
        self._graph.remove_nodes_from(indices)
        return res

    def select_atoms(self, *indices: int) -> List[Atom]:
        """Returns a reference to one or more atoms."""
        return [self._graph.get_node_data(index) for index in indices]

    # TODO: update these upon new retworkx release.

    def insert_bond(self, bond: Bond) -> None:
        """Inserts a bond."""
        self._graph.add_edge(*bond.indices, edge=bond)

    def remove_bond(self, indices: Tuple[int, int]) -> Bond:
        """Removes and returns bonds."""
        res = self._graph.get_edge_data(*indices)
        self._graph.remove_edge(*indices)
        return res

    def select_bond(self, indices: Tuple[int, int]) -> Bond:
        """Returns a mutable reference to a bond."""
        return self._graph.get_edge_data(*indices)

    def to_json(self) -> str:
        """Returns the JSON serialized representation."""
        return json.dumps({
            "atoms": [json.loads(atom.to_json()) for atom in self.atoms],
            "bonds": [json.loads(bond.to_json()) for bond in self.bonds],
        })
