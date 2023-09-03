from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal


class ImagePreviewWidget(QLabel):
    doubleClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setScaledContents(True)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()


class ImagePreview(QWidget):
    _image_preview: QLabel
    doubleClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setLayout(layout)

        self._image_preview = ImagePreviewWidget(self)
        self._image_preview.doubleClicked.connect(
            self._handle_image_preview_double_clicked
        )

        layout.addWidget(self._image_preview)

    def update_image(self, pixmap):
        self._image_preview.setPixmap(pixmap)

    def _handle_image_preview_double_clicked(self):
        self.doubleClicked.emit()
