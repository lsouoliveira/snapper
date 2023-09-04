from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from .widgets.screenshot_dialog import ScreenshotDialog, Region
from .widgets.editor_window import EditorWindow


class App(QApplication):
    def __init__(self):
        super().__init__([])

        self._screenshot_dialog = ScreenshotDialog()
        self._screenshot_dialog.regionChanged.connect(self.region_changed)
        
        self._screenshot_dialog.showFullScreen()

    @QtCore.pyqtSlot(Region)
    def region_changed(self, region):
        self._screenshot_dialog.close()

        pixmap = self._take_screenshot(region)

        if pixmap is None or pixmap.isNull():
            return

        try:
            self.editor_window = EditorWindow(pixmap)
            self.editor_window.showMaximized()
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
            return None
