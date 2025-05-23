from PIL import ImageOps, Image

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class CropImageBorder(Transformation):
    """
    Applies a uniform crop to all sides of the image by removing a fixed-width border.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The config key, "border_crop".
        """
        return "border_crop"

    def apply(self, image: Image.Image, border: int) -> Image.Image:
        """
        Crop a fixed-width border from all sides of the image.

        Args:
            image (Image.Image): The source image.
            border (int): Number of pixels to remove from each side.

        Returns:
            Image.Image: The cropped image.

        Raises:
            TypeError: If `border` is not an integer.
            ValueError: If `border` is less than 1.
        """
        validator = ConfigValidator(key=self.key())
        border = validator.validate_positive_integer(value=border, value_name="border")

        return ImageOps.crop(image=image, border=border)
