# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from .ring_list import RingsListWidget, CrystalItem, ListColumn
from ..func import CrystalsDatabase, CustomCrystal


class DatabaseWindow(RingsListWidget):
    sigCrystalAddedToSelected = pyqtSignal(CustomCrystal)

    _CRYSTAL_COLUMNS = [
        ListColumn(0, lambda crystal: str(crystal.chemical_formula), 'Material'),
        ListColumn(1, lambda crystal: str(crystal.lattice_system.name), 'Structure'),
        ListColumn(2, lambda crystal: str(crystal.source), 'Source'),
    ]

    _RING_COLUMNS = []

    def __init__(self, crystals_database: CrystalsDatabase, parent=None):
        super().__init__(parent,
                         check_boxes=False,
                         expand=False,
                         expand_on_click=False,
                         show_rings_items=False)

        self.crystals_database = crystals_database
        self._connect()

        for crystal in self.crystals_database:
            self.add_crystal(crystal)

    def _on_double_click(self, index):
        item = self.itemFromIndex(index)
        if isinstance(item, CrystalItem):
            self.sigCrystalAddedToSelected.emit(item.crystal)

    def _connect(self):
        self.doubleClicked.connect(self._on_double_click)
        self.crystals_database.sigCrystalAdded.connect(self.add_crystal)
        self.crystals_database.sigCrystalRemoved.connect(self.remove_crystal)
        self.sigCrystalAddedToSelected.connect(self.crystals_database.selected_holder.add_crystal)


class SelectedCrystalsWindow(RingsListWidget):
    def __init__(self, crystals_database: CrystalsDatabase, parent=None):
        super().__init__(parent, check_boxes=True, expand=True, expand_on_click=False)
        self.crystals_database = crystals_database
        self._connect()

    def _connect(self):
        self.crystals_database.selected_holder.sigCrystalAdded.connect(self.add_crystal)
        self.crystals_database.selected_holder.sigCrystalRemoved.connect(self.remove_crystal)
