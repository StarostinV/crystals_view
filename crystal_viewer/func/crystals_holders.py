# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Tuple

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from .custom_crystal import CustomCrystal


class CrystalsHolder(QObject):
    sigCrystalAdded = pyqtSignal(CustomCrystal)
    sigCrystalRemoved = pyqtSignal(CustomCrystal)
    sigErrorCrystalAlreadyExists = pyqtSignal(CustomCrystal)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._crystals: dict = {}

    def __getitem__(self, item):
        return self._crystals[item]

    def __iter__(self):
        yield from self._crystals.values()

    def add_crystal(self, crystal: CustomCrystal):
        if crystal.key not in self._crystals:
            self._crystals[crystal.key] = crystal
            self.sigCrystalAdded.emit(crystal)
        else:
            self.sigErrorCrystalAlreadyExists.emit(crystal)

    @pyqtSlot(object, name='removeCrystal')
    def remove_crystal(self, key: CustomCrystal or str):
        if isinstance(key, CustomCrystal):
            key = key.key
        try:
            self.sigCrystalRemoved.emit(self._crystals.pop(key))
        except KeyError as err:
            raise KeyError(f'Crystal {key} not found') from err

    @pyqtSlot(Path, name='addCrystalFromCif')
    def add_crystal_from_cif(self, cif_path: Path):
        crystal = CustomCrystal.from_cif(str(cif_path.resolve()))
        self.add_crystal(crystal)

    @property
    def crystals(self) -> Tuple[CustomCrystal, ...]:
        return tuple(self._crystals.values())


class SelectedCrystalsHolder(CrystalsHolder):
    def __init__(self, parent):
        super().__init__(parent)
        self._checked_crystals = {}

    @pyqtSlot(str, bool, name='crystalChecked')
    def crystal_checked(self, crystal_key: str, is_checked: bool):
        if is_checked:
            del self._checked_crystals[crystal_key]
        else:
            self._checked_crystals[crystal_key] = self._crystals[crystal_key]

    @property
    def checked_crystals(self) -> Tuple[CustomCrystal, ...]:
        return tuple(self._checked_crystals.values())


class CrystalsDatabase(CrystalsHolder):
    def __init__(self, parent=None):
        super(CrystalsDatabase, self).__init__(parent)
        self.selected_holder = SelectedCrystalsHolder(self)

    @pyqtSlot(object, name='addToSelected')
    def add_to_selected(self, key: CustomCrystal or str):
        if isinstance(key, CustomCrystal):
            key = key.key
        self.selected_holder.add_crystal(self[key])
