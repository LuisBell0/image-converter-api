from .crop import CropImage
from .format import ConvertImageFormat
from .resize import ResizeImage
from .rotate import RotateImage

ALL_TRANSFORMATIONS = [
    ResizeImage(),
    CropImage(),
    RotateImage(),
    ConvertImageFormat(),
]

# Build a dict key → instance:
TRANSFORM_MAP = {t.key(): t for t in ALL_TRANSFORMATIONS}
