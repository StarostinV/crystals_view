# -*- coding: utf-8 -*-

from typing import Tuple
from crystals import Crystal

from .crystal_ring import CrystalRing
from .get_ring_list import get_crystal_rings


class CustomCrystal(Crystal):
    def __init__(self, unitcell, lattice_vectors, source=None, **kwargs):
        super().__init__(unitcell, lattice_vectors, source=source, **kwargs)
        self._key = f'{self.chemical_formula}{self.source}'
        self._rings: Tuple[CrystalRing, ...] = None
        self._q_max: float = 5
        self._min_sf: float = 0.01

    @property
    def rings(self) -> Tuple[CrystalRing, ...]:
        if self._rings is None:
            self._rings = get_crystal_rings(self, self._q_max, self._min_sf)
        return self._rings

    @property
    def key(self) -> str:
        return self._key

    def set_q_max(self, q_max):
        self._q_max = q_max
        self._rings = None

    def set_min_sf(self, min_sf: float):
        if self._rings is not None and min_sf < self._min_sf:
            self._rings = list(filter(lambda ring: ring.intensity >= min_sf, self._rings))
        else:
            self._rings = None
        self._min_sf = min_sf

