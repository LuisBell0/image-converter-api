from PIL import Image

from .transformation_abstract import Transformation
from ..models import FORMAT_CHOICES


class ConvertImageFormat(Transformation):
    """
    Transformation that converts a PIL Image to a specified output format.

    Uses FORMAT_CHOICES from the models to validate allowed output formats.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transform.

        Returns:
            str: The config key, "format".
        """
        return "format"

    def apply(self, image: Image, new_format: str) -> Image:
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
        if not isinstance(new_format, str):
            raise TypeError("Format must be a string")

        valid_formats = {valid_format for valid_format, _ in FORMAT_CHOICES}
        if new_format.upper() not in valid_formats:
            allowed_formats = ', '.join(valid_formats)
            raise ValueError(f'Format must be one of the following formats: {allowed_formats}')
        if not new_format:
            return image

        return image.convert("RGB") if new_format.lower() in ["jpeg", "jpg", "webp"] else image
