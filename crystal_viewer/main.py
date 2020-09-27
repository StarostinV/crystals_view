from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QSplitter
from PyQt5.QtCore import Qt

from .list_widgets import DatabaseWindow, SelectedCrystalsWindow
from .viewer_3d import Crystal3DWidget
from .func import CrystalsDatabase, CustomCrystal
from .file_dialogs import get_cif_folder_dialog, get_cif_file_dialog


class MainCrystalWidget(QWidget):
    def __init__(self, crystals_database: CrystalsDatabase, parent=None):
        super().__init__(parent)
        self.setMinimumSize(700, 700)
        self.database_window = DatabaseWindow(crystals_database, self)
        self.selected_window = SelectedCrystalsWindow(crystals_database, self)
        self.crystal_3d = Crystal3DWidget()

        self._init_ui()
        self._connect()

    def _init_ui(self):
        layout = QGridLayout(self)
        q_splitter = QSplitter(Qt.Horizontal, self)
        q_splitter.setStretchFactor(0, 0.2)
        q_splitter.setStretchFactor(2, 0.7)
        q_splitter.addWidget(self.database_window)
        q_splitter.addWidget(self.selected_window)
        q_splitter.addWidget(self.crystal_3d)
        layout.addWidget(q_splitter)

    def _connect(self):
        self.database_window.sigCrystalSelected.connect(self.crystal_3d.set_crystal)
        self.selected_window.sigCrystalSelected.connect(self.crystal_3d.set_crystal)


class MainCrystalViewer(QMainWindow):
    def __init__(self, crystal_database: CrystalsDatabase = None, parent=None):
        super().__init__(parent)
        self.crystal_database = crystal_database or CrystalsDatabase()
        self.main_widget = MainCrystalWidget(self.crystal_database)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle('Crystal Viewer')
        self.setMinimumSize(700, 500)
        self.setWindowState(Qt.WindowMaximized)
        self._init_menu()

    def _init_menu(self):
        menubar = self.menuBar()
        database = menubar.addMenu('Database')
        add_menu = database.addMenu('Add')
        cif = add_menu.addMenu('Cif files')
        add_cif = cif.addAction('Cif file')
        add_folder = cif.addAction('Folder')
        add_cif.triggered.connect(self._add_cif_file)
        add_folder.triggered.connect(self._add_cif_folder)

        add_crystals_builtins = add_menu.addMenu('Crystals db')
        for name in CustomCrystal.builtins:
            add_crystals_builtins.addAction(name, self._add_builtin(name))

    def _add_cif_file(self):
        path = get_cif_file_dialog(self)
        if path:
            self.crystal_database.add_crystal_from_cif(path)

    def _add_cif_folder(self):
        path = get_cif_folder_dialog(self)
        if path:
            for cif in path.rglob('*.cif'):
                self.crystal_database.add_crystal_from_cif(cif)

    def _add_builtin(self, name: str):
        def func():
            self.crystal_database.add_crystal(CustomCrystal.from_database(name))
        return func
