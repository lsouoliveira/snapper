from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QBuffer
from wand.image import Image

from .image_processor import ImageProcessor


def build_image_processor_from_pixmap(pixmap):
    qt_image = pixmap.toImage()

    buffer = QBuffer()
    buffer.open(QBuffer.WriteOnly)

    qt_image.save(buffer, "PNG")
    image = Image(blob=buffer.data().data())

    return ImageProcessor(image)


def build_pixmap_from_wand_image(image):
    pixmap = QPixmap()
    pixmap.loadFromData(image.make_blob("png"))

    return pixmap
