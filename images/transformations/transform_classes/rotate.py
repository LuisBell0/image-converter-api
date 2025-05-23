from PIL import Image

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class RotateImage(Transformation):
    """
    Transformation that rotates a PIL Image based on the provided angle.

    Optional parameters allow the output size to expand to fit the rotated image,
    and to fill any empty space with a specified color.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The config key, "resize".
        """
        return "rotate"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Apply a rotation transformation to a PIL Image based on the provided configuration.

        Args:
            image (Image.Image): The source PIL Image to transform.
            config (dict): A dictionary with the following optional keys:
                - angle (int or float): The rotation angle in degrees (required).
                - expand (bool): Whether to expand the output image to hold the entire rotated image (default False).
                - fillColor (str, optional): Color string to fill background areas exposed by the rotation (e.g., "white").

        Returns:
            Image.Image: The rotated image.

        Raises:
            TypeError: If config is not a dictionary.
            ValueError: If config is not a dict or contains invalid types for angle, expand, or fillColor.
        """
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)
        validator.validate_required_keys(config_dict=config, required=["angle"])

        angle: int | float = validator.validate_number(value=config.get("angle"), value_name="angle")
        expand: bool = validator.validate_optional_bool(config.get("expand"), value_name="expand")
        fill_color: str | None = validator.validate_optional_str(config.get("fillcolor"), value_name="fillcolor")

        rotate_args: dict = {"angle": angle, "expand": expand}
        if fill_color:
            from PIL import ImageColor
            rotate_args["fillcolor"] = ImageColor.getcolor(color=fill_color, mode='RGB')

        return image.rotate(**rotate_args)
