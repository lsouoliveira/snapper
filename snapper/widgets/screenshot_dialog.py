from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from dataclasses import dataclass


@dataclass
class Region:
    x: int
    y: int
    width: int
    height: int


class ScreenshotDialog(QDialog):
    regionChanged = QtCore.pyqtSignal(Region)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screenshot Widget")
        self.setMinimumSize(800, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: Transparent;")
        self._selected_region = Region(0, 0, 0, 0)

        self._quitShortcut = QShortcut(QKeySequence("Esc"), self)
        self._quitShortcut.activated.connect(self.reject)

    def paintEvent(self, _):
        # draw filled background with opacity
        painter = QPainter(self)

        painter.setBrush(Qt.black)
        painter.setOpacity(0.5)
        painter.drawRect(0, 0, self.width(), self.height())

        # draw selected region
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(
            self._selected_region.x,
            self._selected_region.y,
            self._selected_region.width,
            self._selected_region.height,
        )

        # mask out selected region
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(
            self._selected_region.x,
            self._selected_region.y,
            self._selected_region.width,
            self._selected_region.height,
        )

    def mousePressEvent(self, event):
        self._selected_region.x = event.x()
        self._selected_region.y = event.y()
        self._selected_region.width = 0
        self._selected_region.height = 0

    def mouseMoveEvent(self, event):
        self._selected_region.width = event.x() - self._selected_region.x
        self._selected_region.height = event.y() - self._selected_region.y
        self.update()

    def mouseReleaseEvent(self, _):
        self.regionChanged.emit(self._selected_region)
