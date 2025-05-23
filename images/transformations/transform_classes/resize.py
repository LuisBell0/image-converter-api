from PIL import Image

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class ResizeImage(Transformation):
    """
    Transformation that resizes a PIL Image based on provided width and/or height.

    If only one dimension is provided, the other defaults to the image's original size.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The config key, "resize".
        """
        return "resize"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Resize the input image according to the provided configuration.

        Args:
            image (Image.Image): The source PIL Image to transform.
            config (dict): Dictionary containing resize parameters:
                - width (int): Target width in pixels.
                - height (int): Target height in pixels.

        Returns:
            Image.Image: The resized image.

        Raises:
            TypeError: If config is not a dictionary.
            ValueError: If width or height cannot be converted to an integer.
        """
        print("ran")

        validator = ConfigValidator(self.key())
        config = validator.validate_dictionary(config_dict=config)

        width: int = validator.validate_positive_integer(value=config.get("width", None), value_name="width")
        height: int = validator.validate_positive_integer(value=config.get("height", None), value_name="height")

        return image.resize((width, height))
