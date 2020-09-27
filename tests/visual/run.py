from PyQt5.QtWidgets import QApplication
import sys


def run(widget_class, *args, callback=None, **kwargs):
    qapp = QApplication([])
    widget = widget_class(*args, **kwargs)
    if callback:
        callback(widget)
    widget.show()
    sys.exit(qapp.exec_())
