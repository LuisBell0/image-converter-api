from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class PosterizeImage(Transformation):
    """
    Reduce the number of bits for each color channel, producing a posterized effect.

    Posterization limits the number of color levels by keeping only the most significant
    `bits` for each channel. For example, `bits=4` reduces each channel from 8 bits to 4 bits,
    resulting in 16 discrete levels per channel.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key "posterize".
        """
        return "posterize"

    def apply(self, image: Image.Image, bits: int) -> Image.Image:
        """
        Apply posterization to the provided image.

        Args:
            image (Image.Image): The source PIL image.
            bits (int): Number of bits to keep per channel (1–8).

        Returns:
            Image.Image: A new image with reduced color depth.

        Raises:
            TypeError: If `bits` is not an integer.
            ValueError: If `bits` is outside the valid range [1, 8].
        """
        validator = ConfigValidator(key=self.key())
        bits = validator.validate_positive_integer(value=bits, value_name="bits", max_value=8)

        return ImageOps.posterize(image=image, bits=bits)
