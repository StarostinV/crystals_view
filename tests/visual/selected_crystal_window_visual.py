from pathlib import Path

from crystal_viewer.list_widgets import SelectedCrystalsWindow
from crystal_viewer.func import CrystalsDatabase, CustomCrystal
from tests.visual import run


def callback(selected_window: SelectedCrystalsWindow):
    for crystal in selected_window.crystals_database:
        selected_window.crystals_database.add_to_selected(crystal.key)


def run_selected_crystal_window():
    cif_dir = Path(__file__).parents[2] / 'Cif'

    crystals_database = CrystalsDatabase()
    crystals_database.add_crystal(CustomCrystal.from_database('vo2-rutile'))
    for cif_path in cif_dir.rglob('*.cif'):
        crystals_database.add_crystal_from_cif(cif_path)
    run(SelectedCrystalsWindow, crystals_database=crystals_database, callback=callback)


if __name__ == '__main__':
    run_selected_crystal_window()
