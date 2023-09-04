from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing
from wand.color import Color

from .data.preset import Background, GradientBackground

class ImageProcessor:
    _padding: int
    _border_radius: int
    _background: Background
    _shadow: int

    def __init__(self, source_img):
        self.source_img = source_img
        self._padding = 0
        self._border_radius = 0
        self._shadow = 0
        self._background = Background.create(color="transparent")
        
    def with_padding(self, padding: int):
        self._padding = padding

        return self

    def with_border_radius(self, border_radius: int):
        self._border_radius = border_radius

        return self

    def with_background(self, background: Background):
        self._background = background

        return self

    def with_shadow(self, shadow: int):
        self._shadow = shadow

        return self

    def build(self):
        new_image = Image(width=self.image_width, height=self.image_height)

        self._draw_background(new_image)
        self._draw_image(new_image)

        return new_image

    def _draw_background(self, image):
        bg_image = self._generate_background_image()

        image.composite_channel(
            "default_channels",
            bg_image,
            "over",
            0,
            0,
        )

    @property
    def image_width(self):
        return self.source_img.width + 2 * self._padding

    @property
    def image_height(self):
        return self.source_img.height + 2 * self._padding

    def _generate_background_image(self):
        if isinstance(self._background, GradientBackground):
            image = Image(
                width=self.image_height,
                height=self.image_width,
                pseudo=f"gradient:{self._background.color}-{self._background.second_color}",
            )

            image.rotate(-90)

            return image

        return Image(width=self.image_width, height=self.image_height, background=Color(self._background.color))


    def _draw_image(self, image):
        mask = self._create_radius_mask()

        image_layer = self.source_img.clone()

        image_layer.composite_channel(
            "default_channels",
            mask,
            self._copy_alpha_operator(),
            0,
            0,
        )

        shadow = self.source_img.clone() 
        shadow.background_color = Color("black")
        shadow.shadow(20, self._shadow, 0, 0)

        image.composite_channel(
            "default_channels",
            shadow,
            "over",
            self._padding - 2 * self._shadow,
            self._padding - self._shadow,
        )

        image.composite_channel(
            "default_channels",
            image_layer,
            "over",
            self._padding,
            self._padding,
        )

    def _create_radius_mask(self):
        mask = Image(width=self.source_img.width, height=self.source_img.height, background=Color('transparent'))
        mask.alpha_channel = True

        with Drawing() as draw:
            draw.fill_color = Color("white")
            draw.rectangle(
                left=0,
                top=0,
                width=self.source_img.width,
                height=self.source_img.height,
                radius=self._border_radius if self._border_radius > 0 else None,
            )

            draw(mask)

        return mask

    def _copy_alpha_operator(self):
        if "copy_opacity" in COMPOSITE_OPERATORS:
            return "copy_opacity"
        
        return "copy_alpha"


