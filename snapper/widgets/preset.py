from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal as PyqtSignal

from ..models.preset_model import PresetDTO, PresetModel
from ..data.preset import Background, GradientBackground


class BackgroundOption(QWidget):
    changed = PyqtSignal(Background)

    def __init__(self, background, name, color):
        super().__init__()

        self._background = background
        self._name = name
        self._color = color

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(48)

        self.setLayout(layout)

        self._color_label = QLabel()
        self._color_label.setStyleSheet(
            "font-size: 16px; border-radius: 4px; background: " + self._color + ";"
        )
        self._color_label.setFixedSize(48, 48)
        self._color_label.mousePressEvent = self._on_click

        self._label = QLabel(self._name)
        self._label.setStyleSheet("font-size: 14px; color: #6b7280;")
        self._label.setFixedWidth(48)
        self._label.setWordWrap(True)
        self._label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self._color_label)
        layout.addWidget(self._label)

    def _on_click(self, _):
        self.changed.emit(self._background)


BACKGROUND_OPTIONS = [
    lambda: BackgroundOption(
        background=GradientBackground.create(color="#3494e6", second_color="#ec6ead"),
        name="Vice City",
        color="qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #3494e6, stop: 1 #ec6ead)",
    ),
    lambda: BackgroundOption(
        background=Background.create(color="#00000000"),
        name="None",
        color="#d1d5db",
    ),
]


class Preset(QWidget):
    preset_changed = PyqtSignal(PresetDTO)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = PresetModel()
        self._selected_background = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

        paddingLabel = QLabel("Padding")
        paddingLabel.setStyleSheet("font-size: 16px;")

        self._padding_slider = QSlider(Qt.Horizontal)
        self._padding_slider.setMinimum(0)
        self._padding_slider.setMaximum(256)
        self._padding_slider.setValue(self.model.preset.padding)
        self._padding_slider.sliderReleased.connect(self._update_preset)

        borderRadiusLabel = QLabel("Border Radius")
        borderRadiusLabel.setStyleSheet("font-size: 16px;")

        self._border_radius_slider = QSlider(Qt.Horizontal)
        self._border_radius_slider.setMinimum(0)
        self._border_radius_slider.setMaximum(512)
        self._border_radius_slider.setValue(self.model.preset.padding)
        self._border_radius_slider.sliderReleased.connect(self._update_preset)

        backgroundLabel = QLabel("Background")
        backgroundLabel.setStyleSheet("font-size: 16px;")

        backgroundGrid = QWidget()
        backgroundGridLayout = QVBoxLayout()
        backgroundGridLayout.setContentsMargins(0, 0, 0, 0)
        backgroundGridLayout.setAlignment(Qt.AlignTop)
        backgroundGrid.setLayout(backgroundGridLayout)

        current_row = 0
        max_columns = 5
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setAlignment(Qt.AlignTop)
        row.setSpacing(0)
        backgroundGridLayout.addLayout(row)

        for i, option in enumerate(BACKGROUND_OPTIONS):
            if i % max_columns == 0:
                row = QHBoxLayout()
                row.setContentsMargins(0, 0, 0, 0)
                row.setAlignment(Qt.AlignTop)
                row.setSpacing(0)
                backgroundGridLayout.addLayout(row)

            option = option()
            option.changed.connect(self._handle_background_changed)
            row.addWidget(option)

            if i % max_columns == max_columns - 1:
                current_row += 1
            else:
                row.addStretch()

        if len(BACKGROUND_OPTIONS) > max_columns:
            num_items_to_add = round(len(BACKGROUND_OPTIONS) / max_columns)
        else:
            num_items_to_add = max_columns - len(BACKGROUND_OPTIONS)

        for i in range(num_items_to_add):
            empty = QWidget()
            empty.setFixedWidth(48)

            row.addWidget(empty)

            if i < num_items_to_add:
                row.addStretch()

        layout.addWidget(paddingLabel)
        layout.addWidget(self._padding_slider)
        layout.addWidget(borderRadiusLabel)
        layout.addWidget(self._border_radius_slider)
        layout.addWidget(backgroundLabel)
        layout.addWidget(backgroundGrid)

    def _handle_background_changed(self, background):
        self._selected_background = background
        self._update_preset()

    def _update_preset(self):
        try:
            self.model.update_preset(
                PresetDTO(
                    padding=self._padding_slider.value(),
                    border_radius=self._border_radius_slider.value(),
                    shadow=self.model.preset.shadow,
                    background=self._selected_background
                    or self.model.preset.background,
                )
            )
            self.preset_changed.emit(self.model.preset)
        except ValueError:
            pass
