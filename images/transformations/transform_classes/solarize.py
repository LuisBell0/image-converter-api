from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class SolarizeImage(Transformation):
    """
    Invert all pixel values above a given threshold, producing a “solarized” effect.

    Solarization maps each pixel value v to:
        - v,                if v < threshold
        - 255 – v,          if v >= threshold
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key "solarize".
        """
        return "solarize"

    def apply(self, image: Image.Image, threshold: int = 128) -> Image.Image:
        """
        Apply the solarize effect to the provided image.

        Args:
            image (Image.Image): The source PIL image (mode "L", "RGB", etc.).
            threshold (int):  Threshold for inversion (0–255). Defaults to 128.

        Returns:
            Image.Image: A new image with pixels ≥ threshold inverted.

        Raises:
            TypeError: If `threshold` is not an integer.
            ValueError: If `threshold` is outside the valid range [0, 255].
        """
        validator = ConfigValidator(key=self.key())
        threshold: int = validator.validate_number(
            value=threshold,
            value_name="threshold",
            allowed_types=(int,),
            max_value=255
        )

        return ImageOps.solarize(image=image, threshold=threshold)
