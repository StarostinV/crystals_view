from crystal_viewer.viewer_3d import Crystal3DWidget
from crystal_viewer.list_widgets import DatabaseWindow, SelectedCrystalsWindow
from crystal_viewer.main import MainCrystalViewer
from crystal_viewer.func import CrystalsDatabase


def run():
    import sys
    from PyQt5.QtWidgets import QApplication

    qapp = QApplication([])
    database = CrystalsDatabase()
    main_window = MainCrystalViewer(database)
    main_window.show()

    try:
        import qdarkgraystyle as style

        stylesheet = style.load_stylesheet()
        qapp.setStyleSheet(stylesheet)
    except ImportError:
        style = None

    sys.exit(qapp.exec_())


if __name__ == '__main__':
    run()
