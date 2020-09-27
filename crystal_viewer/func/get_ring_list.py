# -*- coding: utf-8 -*-


from typing import List, Tuple
import cmath
import numpy as np

from crystals import Crystal
from periodictable import cromermann as cr_ff

from .crystal_ring import CrystalRing


def get_crystal_rings(crystal: Crystal, q_max: float, min_sf: float = 0.01) -> Tuple[CrystalRing, ...]:
    ring_list: List[CrystalRing] = []
    atom_list = [(str(atom), atom.coords_fractional) for atom in crystal]

    for miller_indices in crystal.bounded_reflections(q_max):
        if np.all(np.array(miller_indices) >= 0):
            scattering_vector = crystal.scattering_vector(miller_indices)
            q = np.linalg.norm(scattering_vector)
            sf = _calc_structure_factor(scattering_vector, miller_indices, atom_list)
            if sf >= min_sf:
                ring_list.append(CrystalRing(radius=q,
                                             miller_indices=miller_indices,
                                             intensity=sf,
                                             crystal=crystal))
    ring_list.sort(key=lambda ring: ring.radius)
    return tuple(ring_list)


def _calc_structure_factor(scattering_vector, miller_indices, atom_list):
    q = np.linalg.norm(scattering_vector)
    sf = 0
    for (element, coords_fractional) in atom_list:
        ff = cr_ff.fxrayatq(element, q, charge=None)
        sf = sf + ff * cmath.exp(2 * np.pi * 1j * np.dot(miller_indices, coords_fractional))
    return abs(sf)
