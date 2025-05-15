from .crop import CropImage
from .enhancements import SharpnessEnhancement, ColorEnhancement, BrightnessEnhancement, ContrastEnhancement
from .format import ConvertImageFormat
from .resize import ResizeImage
from .rotate import RotateImage
from .transpose import TransposeImage

# TODO: UPDATE FOR DYNAMIC IMPORT AND REGISTER INSTEAD OF MANUALLY REGISTER EACH TRANSFORMATION

ALL_TRANSFORMATIONS = [
    ResizeImage(),
    CropImage(),
    RotateImage(),
    TransposeImage(),
    ContrastEnhancement(),
    BrightnessEnhancement(),
    SharpnessEnhancement(),
    ColorEnhancement(),
    ConvertImageFormat(),
]

# Build a dict key → instance:
TRANSFORM_MAP = {t.key(): t for t in ALL_TRANSFORMATIONS}
