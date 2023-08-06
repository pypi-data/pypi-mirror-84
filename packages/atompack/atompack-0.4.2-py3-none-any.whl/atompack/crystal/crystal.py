"""Abstractions for unit cells and crystals.
Unit cells act as templates to create crystals with arbitrary transformations applied to them."""

import copy
import json

import numpy as np

from atompack.atom import Atom
from atompack.bond import Bond
from atompack.crystal.components import (Basis, LatticeParameters, LatticeVectors)
from atompack.symmetry import Spacegroup
from atompack.topology import Topology


class UnitCell(Topology):
    """Minimal representation of a crystalline structure.
    
    Args:
        basis: Atomic basis.
        lattice_parameters: Lattice parameters object.
        spacegroup: Spacegroup object.

    Example:
        >>> # primitive basis of iron
        >>> basis = Basis.primitive("Fe")
        >>> 
        >>> # cubic lattice parameters
        >>> lattparams = LatticeParameters.cubic(2.85)
        >>> 
        >>> # BCC spacegroup
        >>> spg = Spacegroup("I m -3 m")
        >>> 
        >>> # build the unit cell
        >>> unit_cell = UnitCell(basis, lattparams, spg)
        >>> assert len(unit_cell.atoms) == 2
    """

    def __init__(
        self,
        basis: Basis,
        lattice_parameters: LatticeParameters,
        spacegroup: Spacegroup,
        _build: bool = True,
    ) -> None:
        # initialize superclass
        super().__init__()
        # set attributes
        self._basis = basis
        self._lattice_parameters = lattice_parameters
        self._spacegroup = spacegroup
        # build the unit cell
        if _build:
            self._build()

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_json(cls, s: str) -> 'UnitCell':
        """Initializes from a JSON string."""
        topology = Topology.from_json(s)
        data = json.loads(s)
        basis = Basis.from_json(json.dumps(data["basis"]))
        params = LatticeParameters.from_json(json.dumps(data["lattice_parameters"]))
        spg = Spacegroup(int(data["spacegroup"]))
        # initialize unit cell without placing atoms
        res = cls(basis, params, spg, _build=False)
        res._graph = topology._graph
        return res

    ####################
    #    Properties    #
    ####################

    @property
    def basis(self) -> Basis:
        """Returns the basis."""
        return self._basis

    @property
    def lattice_parameters(self) -> LatticeParameters:
        """Returns the lattice parameters."""
        return self._lattice_parameters

    @property
    def spacegroup(self) -> Spacegroup:
        """Returns the spacegroup."""
        return self._spacegroup

    ########################
    #    Public Methods    #
    ########################

    def to_json(self) -> str:
        """Returns the JSON serialized representation."""
        topology_data = json.loads(super().to_json())
        return json.dumps({
            "basis": json.loads(self.basis.to_json()),
            "lattice_parameters": json.loads(self.lattice_parameters.to_json()),
            "spacegroup": self.spacegroup.international_number,
            "atoms": topology_data["atoms"],
            "bonds": topology_data["bonds"],
        })

    #########################
    #    Private Methods    #
    #########################

    def _build(self) -> None:
        vectors = LatticeVectors.from_lattice_parameters(self.lattice_parameters).vectors
        for specie, site in self.basis.apply_spacegroup(self.spacegroup):
            position = site * np.linalg.norm(vectors, axis=0)
            self.insert_atoms(Atom(specie, position))


class Crystal(Topology):
    """Atomic structure with long range order.
    
    Args:
        unit_cell: Minimal representation of a crystalline structure.
    """

    def __init__(
        self,
        unit_cell: UnitCell,
        _build: bool = True,
    ) -> None:
        # initialize superclass
        super().__init__()
        # build the crystal
        self._unit_cell = unit_cell
        if _build:
            self._lattice_vectors = LatticeVectors.from_lattice_parameters(self._unit_cell.lattice_parameters)
            for atom in self._unit_cell.atoms:
                self.insert_atoms(copy.deepcopy(atom))
            for bond in self._unit_cell.bonds:
                self.insert_bond(copy.deepcopy(bond))

    ######################
    #    Constructors    #
    ######################

    @classmethod
    def from_json(cls, s: str) -> 'Crystal':
        """Initializes from a JSON string."""
        topology = Topology.from_json(s)
        data = json.loads(s)
        unit_cell = UnitCell.from_json(json.dumps(data["unit_cell"]))
        res = cls(unit_cell, _build=False)
        res._lattice_vectors = LatticeVectors.from_json(json.dumps(data["lattice_vectors"]))
        res._graph = topology._graph
        return res

    ####################
    #    Properties    #
    ####################

    @property
    def lattice_vectors(self):
        """Returns the lattice vectors."""
        return self._lattice_vectors

    @property
    def unit_cell(self):
        """Returns the unit cell."""
        return self._unit_cell

    ########################
    #    Public Methods    #
    ########################

    def to_json(self) -> str:
        """Returns the JSON serialized representation."""
        topology_data = json.loads(super().to_json())
        return json.dumps({
            "unit_cell": json.loads(self.unit_cell.to_json()),
            "lattice_vectors": json.loads(self.lattice_vectors.to_json()),
            "atoms": topology_data["atoms"],
            "bonds": topology_data["bonds"],
        })
