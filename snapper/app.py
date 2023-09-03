from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from .widgets.screenshot_dialog import ScreenshotDialog, Region
from .widgets.editor_window import EditorWindow


class App(QApplication):
    def __init__(self):
        super().__init__([])

        # self._screenshot_dialog = ScreenshotDialog()
        # self._screenshot_dialog.regionChanged.connect(self.region_changed)
        #
        # self._screenshot_dialog.show()
        self.editor_window = EditorWindow(None)
        self.editor_window.show()

    @QtCore.pyqtSlot(Region)
    def region_changed(self, region):
        self._screenshot_dialog.close()

        pixmap = self._take_screenshot(region)

        if pixmap.isNull():
            return

        try:
            self.editor_window = EditorWindow(pixmap)
            self.editor_window.show()
        except Exception as _:
            return


    def _take_screenshot(self, region):
        try:
            return self.primaryScreen().grabWindow(
                0,
                region.x + self._screenshot_dialog.x(),
                region.y + self._screenshot_dialog.y(),
                region.width,
                region.height,
            )
        except Exception as _:
            return None
