from PIL import ImageOps, Image

from images.transformations.registry import register_transform
from images.transformations.transformation_abstract import Transformation


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
        if not isinstance(border, int):
            raise TypeError(f"{self.key()} value must be an integer")
        if border < 1:
            raise ValueError(f"{self.key()} value must be a positive integer")

        return ImageOps.crop(image=image, border=border)
