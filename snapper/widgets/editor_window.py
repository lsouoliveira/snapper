from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from .image_preview import ImagePreview
from .preset import Preset 
from ..utils import build_image_processor_from_pixmap, build_pixmap_from_wand_image

class EditorWindow(QMainWindow):
    _image_preview: ImagePreview

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)

        self._pixmap = pixmap
        self._image_processor = build_image_processor_from_pixmap(self._pixmap)
        self._update_preview_timer = None

        self.setWindowTitle("Snapper")
        self.setMinimumSize(800, 600)
        self._setup_ui()

        self._copyShortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self._copyShortcut.activated.connect(self.copy_to_clipboard)
        self._update_image_preview(self._preset.model.preset)

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
        self.copy_to_clipboard()
        self.close()

    def copy_to_clipboard(self):
        QApplication.clipboard().setPixmap(self._image_preview.image)


    def _handle_preset_changed(self, preset):
        self._update_image_preview(preset)

    def _update_image_preview(self, preset):
        updated_image = (
            self._image_processor.with_padding(preset.padding)
            .with_border_radius(preset.border_radius)
            .with_background(preset.background)
            .with_shadow(preset.shadow)
            .build()
        )

        pixmap = build_pixmap_from_wand_image(updated_image)

        self._image_preview.update_image(pixmap)
