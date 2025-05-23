from PIL import Image

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator

TRANSPOSE_METHODS = {
    'FLIP_LEFT_RIGHT': Image.Transpose.FLIP_LEFT_RIGHT,
    'FLIP_TOP_BOTTOM': Image.Transpose.FLIP_TOP_BOTTOM,
    'ROTATE_180': Image.Transpose.ROTATE_180,
    'ROTATE_270': Image.Transpose.ROTATE_270,
    'ROTATE_90': Image.Transpose.ROTATE_90,
    'TRANSPOSE': Image.Transpose.TRANSPOSE,
    'TRANSVERSE': Image.Transpose.TRANSVERSE,
}


@register_transform
class TransposeImage(Transformation):
    """
    Transformation that applies a predefined transpose operation to a PIL Image.

    Transpose operations include flips and 90/180/270 degree rotations, as well as
    transpositions. The operation is chosen via a string identifier.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The config key, "transpose".
        """
        return "transpose"

    def apply(self, image: Image.Image, transpose_method: str) -> Image.Image:
        """
        Apply a transpose transformation to a PIL Image based on the provided configuration.

        Args:
            image (Image.Image): The input PIL Image to transform.
            transpose_method (str): The transpose method name, one of:
                "FLIP_LEFT_RIGHT", "FLIP_TOP_BOTTOM",
                "ROTATE_90", "ROTATE_180", "ROTATE_270",
                "TRANSPOSE", "TRANSVERSE"

        Returns:
            Image.Image: The transformed image.

        Raises:
            ValueError: transpose_method is None, not a string or not in TRANSPOSE_METHODS.
        """
        validator = ConfigValidator(key=self.key())
        transpose_method = validator.validate_choice(
            value=transpose_method,
            value_name="transpose_method",
            options=list(TRANSPOSE_METHODS.keys())
        )

        return image.transpose(TRANSPOSE_METHODS[transpose_method])
