from .crop import CropImage
from .format import ConvertImageFormat
from .resize import ResizeImage

ALL_TRANSFORMATIONS = [
    ConvertImageFormat(),
    ResizeImage(),
    CropImage(),
]

# Build a dict key → instance:
TRANSFORM_MAP = {t.key(): t for t in ALL_TRANSFORMATIONS}
