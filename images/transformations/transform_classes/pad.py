from PIL import Image, ImageOps

from images.transformations.filters_mapping import RESAMPLING_FILTERS
from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class PadImage(Transformation):
    """
    Pad or crop an image to a specified size, preserving aspect ratio and centering.

    This transform resizes and/or pads the input image to fit exactly into the
    target size. If the image is smaller, it will be padded with the given color;
    if larger, it will be cropped. The original aspect ratio is preserved.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key "pad".
        """
        return "pad"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Apply padding or cropping to the provided image.

        Args:
            image (Image.Image): The source PIL image.
            config (dict): Must contain:
                - size (Tuple[int, int]): Target dimensions.
            Optional keys:
                - method (str): Resampling filter name.
                - color (int, str, or tuple): Padding fill color.
                - centering (Tuple[float, float]): Centering factors.

        Returns:
            Image.Image: A new image of size `size`.

        Raises:
            TypeError: If `config` is not a dict or contains wrong types.
            ValueError: If numeric values are out of allowed ranges.
        """
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)
        validator.validate_required_keys(config_dict=config, required=["size"])

        size: tuple[int, int] = validator.validate_number_tuple(
            value=config.get("size"),
            value_name="size",
            allowed_types=(int,),
            length=2
        )

        method_key: str = validator.validate_choice(
            value=config.get('method', 'BICUBIC'),
            value_name="method",
            options=list(RESAMPLING_FILTERS.keys())
        )

        resample_filter: int = RESAMPLING_FILTERS[method_key]

        color: str | int | tuple[int, ...] | None = validator.validate_color(
            value=config.get('color', 0),
            value_name="color"
        )

        centering: tuple[float, float] = self.validate_centering(
            value=config.get('centering', (0.5, 0.5)),
            validator=validator,
            value_name="centering"
        )

        return ImageOps.pad(
            image,
            size=size,
            method=resample_filter,
            color=color,
            centering=centering
        )

    @staticmethod
    def validate_centering(
            value: tuple[float, float],
            validator: ConfigValidator,
            value_name: str = "Value"
    ) -> tuple[float, float]:
        """
        Validate that `value` is a 2-tuple (or list) of numbers between 0.0 and 1.0.

        Args:
            value (tuple[float, float]): The value to validate.
            validator (ConfigValidator): Validator instance for checking.
            value_name (str): The name of the value to validate.

        Returns:
             tuple[float, float]: The normalized value as a (float, float) tuple.
        """
        value = validator.validate_number_tuple(value=value, value_name=value_name, allowed_types=(float,), length=2)
        center_x, center_y = value

        if not (0.0 <= center_x <= 1.0 and 0.0 <= center_y <= 1.0):
            raise ValueError(validator.error(
                value_name=value_name,
                message=f"values must be between 0.0 and 1.0; got {value!r}"
            ))

        return float(center_x), float(center_y)
