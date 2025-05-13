from .crop import CropImage
from .format import ConvertImageFormat
from .resize import ResizeImage
from .rotate import RotateImage
from .transpose import TransposeImage

ALL_TRANSFORMATIONS = [
    ResizeImage(),
    CropImage(),
    RotateImage(),
    TransposeImage(),
    ConvertImageFormat(),
]

# Build a dict key → instance:
TRANSFORM_MAP = {t.key(): t for t in ALL_TRANSFORMATIONS}
