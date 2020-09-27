from crystals import Crystal

from crystal_viewer.viewer_3d import Crystal3DWidget
from tests.visual import run


def callback(widget: Crystal3DWidget):
    widget.set_crystal(Crystal.from_database('vo2-rutile'))


def visual_crystal_3d():
    run(Crystal3DWidget, callback=callback)


if __name__ == '__main__':
    visual_crystal_3d()
