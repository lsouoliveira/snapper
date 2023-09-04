from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing
from wand.color import Color

from .data.preset import Background, GradientBackground

def image_to_pixels(image):
    pixels = image.export_pixels()

    return [tuple(pixels[i:i + 4]) for i in range(0, len(pixels), 4)]

def color_from_tuple(t):
    return Color("rgba({}, {}, {}, {})".format(*t))

class ImageProcessor:
    _padding: int
    _border_radius: int
    _background: Background
    _shadow: int
    _inset: int

    def __init__(self, source_img):
        self.source_img = source_img
        self._padding = 0
        self._border_radius = 0
        self._shadow = 0
        self._inset = 0
        self._background = Background.create(color="transparent")
        self._pixels = image_to_pixels(self.source_img) 
        self._edge_color = color_from_tuple(self.edge_color())

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
    
    def with_inset(self, inset: int):
        self._inset = inset

        return self

    def build(self):
        new_image = Image(width=self.image_width, height=self.image_height)

        self._draw_background(new_image)
        self._draw_image(new_image)

        return new_image

    @property
    def vertical_padding(self):
        return self._padding 

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
        return self.source_img.width + 2 * self._padding + 2 * self._inset

    @property
    def image_height(self):
        return self.source_img.height + 2 * self._padding + 2 * self._inset
    
    def edge_color(self):
        width = self.source_img.width
        height = self.source_img.height

        top_pixels = [self._pixels[i] for i in range(width)]
        right_pixels = [self._pixels[i * width + width - 1] for i in range(height)]
        left_pixels = [self._pixels[i * width] for i in range(height)]
        bottom_pixels = [self._pixels[(height - 1 ) * width + i] for i in range(width)]

        pixels = top_pixels + right_pixels + left_pixels + bottom_pixels

        return max(set(pixels), key=pixels.count)

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

        if self._shadow > 0:
            with Drawing() as draw:
                shadow = Image(width=self.source_img.width + 2 * self._inset, height=self.source_img.height + 2 * self._inset) 
                shadow.background_color = Color("black")

                draw.fill_color = Color("black") 
                draw.rectangle(
                    left=0,
                    top=0,
                    width=shadow.width,
                    height=shadow.height,
                    radius=self._border_radius if self._border_radius > 0 else None,
                )

                draw(shadow)

                shadow.shadow(40, self._shadow, 0, 0)

                image.composite_channel(
                    "default_channels",
                    shadow,
                    "over",
                    self._padding - 2 * self._shadow,
                    self.vertical_padding - self._shadow,
                )

        with Drawing() as draw:
            draw.fill_color = self._edge_color 
            draw.rectangle(
                left=self._padding,
                top=self.vertical_padding,
                width=self.source_img.width + 2 * self._inset,
                height=self.source_img.height + 2 * self._inset,
                radius=self._border_radius if self._border_radius > 0 else None,
            )

            draw(image)


        image.composite_channel(
            "default_channels",
            image_layer,
            "over",
            self._padding + self._inset,
            self.vertical_padding + self._inset,
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
                radius=self._border_radius if self._border_radius > 0 and self._inset <= 0 else None,
            )

            draw(mask)

        return mask

    def _copy_alpha_operator(self):
        if "copy_opacity" in COMPOSITE_OPERATORS:
            return "copy_opacity"
        
        return "copy_alpha"


