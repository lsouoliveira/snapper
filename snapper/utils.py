from PyQt5.QtGui import QPixmap, QImage
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
    image_bytes = image.make_blob(format="RGBA")
    qt_image = QImage(image_bytes, image.width, image.height, QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(qt_image)

    return pixmap
