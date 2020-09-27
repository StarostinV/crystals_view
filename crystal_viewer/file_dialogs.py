from pathlib import Path

from PyQt5.QtWidgets import QFileDialog


def get_filepath_dialog(parent, message: str, formats: str):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filepath, _ = QFileDialog.getOpenFileName(
        parent, message, '',
        formats, options=options)
    if filepath:
        return Path(filepath)


def get_cif_folder_dialog(parent) -> Path or None:
    return get_folder_filepath(parent, message='Choose folder containing cif files.')


def get_cif_file_dialog(parent) -> Path or None:
    return get_filepath_dialog(parent, 'Select cif file', 'Cif file (*.cif)')


def get_folder_filepath(parent, message: str, *, show_files: bool = True,
                        directory: str = '', exists: bool = True) -> Path or None:
    options = QFileDialog.DontResolveSymlinks | QFileDialog.DontUseNativeDialog
    if not show_files:
        options |= QFileDialog.ShowDirsOnly

    dialog = QFileDialog(parent, caption=message, directory=directory)
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOptions(options)

    if not exists:
        dialog.setAcceptMode(QFileDialog.AcceptSave)

    if dialog.exec_() == QFileDialog.Accepted:
        folder_path = dialog.selectedFiles()[0]

        if folder_path:
            return Path(folder_path)
