from PIL import Image, ImageEnhance

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


class ImageEnhancer(Transformation):
    """
    A generic image-enhancement transformation.

    Wraps any of PIL's ImageEnhance factories (Brightness, Sharpness, Color,
    Contrast, etc.) and applies the selected enhancement based on a provided
    numeric factor.

    Attributes:
        _key (str): The configuration key name for this transformation.
        _enhancer_class (Type[ImageEnhance.ImageEnhance]): The PIL ImageEnhance
            class used to perform the enhancement.
    """

    def __init__(
        self,
        key_name: str,
        enhancer_class: ImageEnhance,
    ):
        super().__init__()
        self._key = key_name
        self._enhancer_class = enhancer_class

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key name provided at initialization.
        """
        return self._key

    def apply(self, image: Image.Image, factor: float | int) -> Image.Image:
        """
        Apply the enhancement to the given PIL image.

        Args:
            image (Image.Image): The source image to transform.
            factor (int or float): A non-negative numeric factor.
                Values > 1 amplify the effect (e.g., brighter, sharper),
                values < 1 reduce/mute the effect.

        Returns:
            Image.Image: A new PIL image with the enhancement applied.

        Raises:
            ValueError: If `enhancement_value` is not an int or float, or if it is
                negative.
        """
        validator = ConfigValidator(key=self.key())
        enhancement_value = validator.validate_number(
            value=factor,
            value_name="enhancement_value",
            min_value=0
        )

        enhancer = self._enhancer_class(image)
        return enhancer.enhance(enhancement_value)


@register_transform
class SharpnessEnhancement(ImageEnhancer):
    """
    Adjust sharpness of an image.

    Uses PIL.ImageEnhance.Sharpness to modify the sharpness level.
    """
    def __init__(self):
        super().__init__(key_name="sharpness", enhancer_class=ImageEnhance.Sharpness)


@register_transform
class BrightnessEnhancement(ImageEnhancer):
    """
    Adjust brightness of an image.

    Uses PIL.ImageEnhance.Brightness to modify the brightness level.
    """
    def __init__(self):
        super().__init__(key_name="brightness", enhancer_class=ImageEnhance.Brightness)


@register_transform
class ContrastEnhancement(ImageEnhancer):
    """
    Adjust contrast of an image.

    Uses PIL.ImageEnhance.Contrast to modify the contrast level.
    """
    def __init__(self):
        super().__init__(key_name="contrast", enhancer_class=ImageEnhance.Contrast)


@register_transform
class ColorEnhancement(ImageEnhancer):
    """
    Enhance color intensity of an image.

    Uses PIL.ImageEnhance.Color to adjust color balance and intensity.
    """
    def __init__(self):
        super().__init__(key_name="color", enhancer_class=ImageEnhance.Color)
