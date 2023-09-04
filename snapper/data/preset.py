class NaturalNumber:
    _value: int

    def __init__(self, value):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @staticmethod
    def create(value: int) -> "NaturalNumber":
        if value < 0:
            raise ValueError("value must be positive")

        return NaturalNumber(value=int(value))


class Background:
    _color: str

    def __init__(self, color: str):
        self._color = color

    @property
    def color(self) -> str:
        return self._color

    @staticmethod
    def create(color: str) -> "Background":
        return Background(color=color)


class GradientBackground(Background):
    _second_color: str

    def __init__(self, color: str, second_color: str):
        super().__init__(color=color)
        self._second_color = second_color

    @property
    def second_color(self) -> str:
        return self._second_color

    @staticmethod
    def create(color: str, second_color: str) -> "GradientBackground":
        return GradientBackground(color=color, second_color=second_color)


class Preset:
    _padding: NaturalNumber
    _border_radius: NaturalNumber
    _shadow: NaturalNumber
    _background: Background
    _inset: NaturalNumber

    def __init__(
        self,
        padding: NaturalNumber,
        border_radius: NaturalNumber,
        shadow: NaturalNumber,
        background: Background,
        inset: NaturalNumber
    ):
        self._padding = padding
        self._border_radius = border_radius
        self._shadow = shadow
        self._background = background
        self._inset = inset

    @property
    def padding(self) -> int:
        return self._padding.value

    @property
    def border_radius(self) -> int:
        return self._border_radius.value

    @property
    def shadow(self) -> int:
        return self._shadow.value

    @property
    def background(self) -> Background:
        return self._background

    @property
    def inset(self) -> int:
        return self._inset.value

    @staticmethod
    def create(
        padding: NaturalNumber,
        border_radius: NaturalNumber,
        shadow: NaturalNumber,
        background: Background,
        inset: NaturalNumber
    ) -> "Preset":
        return Preset(
            padding=padding,
            border_radius=border_radius,
            shadow=shadow,
            background=background,
            inset=inset
        )
