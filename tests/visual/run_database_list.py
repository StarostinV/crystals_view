from pathlib import Path

from crystal_viewer.list_widgets import DatabaseWindow
from crystal_viewer.func import CrystalsDatabase, CustomCrystal
from tests.visual import run


def run_selected_crystal_window():
    cif_dir = Path(__file__).parents[2] / 'Cif'

    crystals_database = CrystalsDatabase()
    crystals_database.add_crystal(CustomCrystal.from_database('vo2-rutile'))
    for cif_path in cif_dir.rglob('*.cif'):
        crystals_database.add_crystal_from_cif(cif_path)
    run(DatabaseWindow, crystals_database=crystals_database)


if __name__ == '__main__':
    run_selected_crystal_window()
