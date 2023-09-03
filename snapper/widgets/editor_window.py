from PyQt5.QtCore import QBuffer, QByteArray, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from wand.image import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
import requests

from .image_preview import ImagePreview
from .preset import Preset
from ..image_processor import ImageProcessor
from ..utils import build_image_processor_from_pixmap, build_pixmap_from_wand_image


class EditorWindow(QMainWindow):
    _image_preview: ImagePreview

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)

        self._pixmap = QPixmap(self._load_test_image())
        self._image_processor = build_image_processor_from_pixmap(self._pixmap)
        self._update_preview_timer = None

        self.setWindowTitle("Snapper")
        self.setMinimumSize(800, 600)
        self._setup_ui()

        self._image_preview.update_image(self._pixmap)

    def _setup_ui(self):
        central_widget = QWidget()

        layout = QHBoxLayout()
        layout.setStretch(0, 1)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Image space
        self._image_preview = ImagePreview(self)
        self._image_preview.doubleClicked.connect(
            self._handle_image_preview_double_clicked
        )

        # Preset space
        self._preset = Preset(self)
        self._preset.setFixedWidth(300)
        self._preset.preset_changed.connect(self._handle_preset_changed)

        layout.addWidget(self._image_preview)
        layout.addWidget(self._preset)

    def _handle_image_preview_double_clicked(self):
        self.close()

    def _handle_preset_changed(self, preset):
        if self._update_preview_timer is not None:
            self._update_preview_timer.stop()

        self._update_preview_timer = QTimer()
        self._update_preview_timer.setSingleShot(True)
        self._update_preview_timer.timeout.connect(
            lambda: self._update_image_preview(preset)
        )
        self._update_preview_timer.start(500)

    def _update_image_preview(self, preset):
        updated_image = (
            self._image_processor.with_padding(preset.padding)
            .with_border_radius(preset.border_radius)
            .with_background(preset.background)
            .build()
        )
        pixmap = build_pixmap_from_wand_image(updated_image)

        self._image_preview.update_image(pixmap)

    def _load_test_image(self):
        data = requests.get(
            "https://learn.microsoft.com/pt-br/education/windows/images/windows-11-se.png"
        ).content

        return QImage.fromData(data)
