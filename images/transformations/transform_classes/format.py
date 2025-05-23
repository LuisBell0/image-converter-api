from PIL import Image

from images.models import FORMAT_CHOICES
from images.transformations.registry import register_transform
from images.transformations.validators import ConfigValidator
from .transformation_abstract import Transformation


@register_transform
class ConvertImageFormat(Transformation):
    """
    Transformation that converts a PIL Image to a specified output format.

    Uses FORMAT_CHOICES from the models to validate allowed output formats.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The config key, "format".
        """
        return "format"

    def apply(self, image: Image.Image, new_format: str) -> Image.Image:
        """
        Convert the input image to a specified format.

        Args:
            image (Image.Image): The source PIL Image to transform.
            new_format (str): The target format (e.g., 'JPEG', 'PNG', 'WEBP').

        Returns:
            Image.Image: The converted image, or the original image if new_format is falsy.

        Raises:
            TypeError: If `new_format` is not a string.
            ValueError: If `new_format` is not one of the allowed formats.
        """
        validator = ConfigValidator(key=self.key())
        valid_formats = list({valid_format for valid_format, _ in FORMAT_CHOICES})
        new_format = validator.validate_choice(value=new_format, options=valid_formats)

        return image.convert("RGB") if new_format.lower() in ["jpeg", "jpg", "webp"] else image
