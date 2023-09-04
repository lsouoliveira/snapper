from PyQt5.QtCore import QObject, pyqtSignal
from dataclasses import dataclass

from ..data.preset import NaturalNumber, Preset, Background, GradientBackground


@dataclass
class PresetDTO:
    padding: int
    border_radius: int
    shadow: int
    background: Background


class PresetModel(QObject):
    preset_changed = pyqtSignal(PresetDTO)

    def __init__(self):
        super().__init__()

        self._preset = Preset.create(
            padding=NaturalNumber(96),
            border_radius=NaturalNumber(32),
            shadow=NaturalNumber(0),
            background=GradientBackground.create(color="#3494e6", second_color="#ec6ead"),
        )

    @property
    def preset(self) -> PresetDTO:
        return self.map_preset_to_preset_dto(self._preset)

    def update_preset(self, preset: PresetDTO):
        self._preset = Preset.create(
            padding=NaturalNumber(preset.padding),
            border_radius=NaturalNumber(preset.border_radius),
            shadow=NaturalNumber(preset.shadow),
            background=preset.background,
        )
        self.preset_changed.emit(self.map_preset_to_preset_dto(self._preset))

    @staticmethod
    def map_preset_to_preset_dto(preset: Preset) -> PresetDTO:
        return PresetDTO(
            padding=preset.padding,
            border_radius=preset.border_radius,
            shadow=preset.shadow,
            background=preset.background,
        )
