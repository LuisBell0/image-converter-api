from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class ExpandImage(Transformation):
    """
    Add a border (padding) around an image.

    This transform increases the canvas size by adding a colored border
    around the original image.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key "expand".
        """
        return "expand"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Apply border expansion to the provided image.

        Args:
            image (Image.Image): The source PIL image.
            config (dict): Must contain:
                - "border": int >= 0, or tuple of four ints >= 0.
                - "fill": (optional) int, str, or tuple specifying border color.

        Returns:
            Image.Image: A new image with the specified border.

        Raises:
            TypeError: If `config` is not a dict, or types of `border`/`fill` are incorrect.
            ValueError: If `border` values are negative, or tuple length is not 4.
        """
        validator = ConfigValidator(key=self.key())

        config = validator.validate_dictionary(config_dict=config)
        validator.validate_required_keys(config_dict=config, required=["border"])

        border: int | tuple[int, ...] = self.validate_border(value=config.get("border"), validator=validator)

        fill: str | int | tuple[int, ...] = validator.validate_color(value=config.get("fill", 0), value_name="fill")

        return ImageOps.expand(image, border=border, fill=fill)

    @staticmethod
    def validate_border(value: int | tuple[int, ...], validator: ConfigValidator) -> int | tuple[int, ...]:
        """
        Validates the `border` value, ensuring it is either a non-negative integer or a 4-tuple of non-negative integers.

        Args:
            value (int or tuple of int): The border value to validate.
            validator (ConfigValidator): Validator instance for type and range checking.

        Returns:
            int or tuple of int: The validated border value.

        Raises:
            ValueError: If the integer is negative or the tuple contains invalid values.
            TypeError: If the value is not an integer or a 4-tuple/list of integers.
        """
        validator.ensure_type(value=value, types=(int, tuple), value_name="border")
        if isinstance(value, int):
            if value < 0:
                raise ValueError(validator.error(value_name="border", message=f"must be non-negative; got {value}"))
            return value

        if isinstance(value, (tuple, list)):
            validated = validator.validate_number_tuple(
                value=value,
                value_name="border",
                allowed_types=(int,),
                length=4
            )
            return tuple(validated)

        raise TypeError(validator.error(
            value_name="border",
            message=f"must be an int or 4-tuple of ints; got {type(value).__name__}")
        )
