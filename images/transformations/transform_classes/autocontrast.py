from collections.abc import Sequence

from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class AutocontrastImage(Transformation):
    """
    Applies an autocontrast transformation to a PIL image.

    This class enhances the contrast of an image by remapping the pixel values
    so that the darkest becomes black and the lightest becomes white, optionally
    ignoring certain pixel values and preserving the original tone.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key "autocontrast".
        """
        return "autocontrast"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Applies the autocontrast transformation using the provided configuration.

        Args:
            image (PIL.Image.Image): The image to transform.
            config (dict): A configuration dictionary containing:
                - cutoff (float or tuple of float): Percentage to cut off from histogram.
                - ignore (int or list of int, optional): Pixel value(s) to ignore.
                - preserve_tone (bool, optional): Whether to preserve the overall tone.

        Returns:
            PIL.Image.Image: The transformed image with enhanced contrast.

        Raises:
            ValueError: If the configuration contains invalid types or values.
        """
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)
        validator.validate_required_keys(config_dict=config, required=["cutoff"])

        cutoff: float | tuple[float, float] = self.validate_cutoff(
            value=config.get("cutoff"),
            validator=validator,
            value_name="cutoff"
        )

        ignore: int | Sequence[int] | None = self.validate_ignore(
            value=config.get("ignore"),
            validator=validator,
            value_name="ignore"
        )

        preserve_tone: bool = validator.validate_optional_bool(
            value=config.get("preserve_tone"),
            value_name="preserve_tone"
        )

        return ImageOps.autocontrast(image=image, cutoff=cutoff, ignore=ignore, preserve_tone=preserve_tone)

    @staticmethod
    def validate_cutoff(
            value: float | tuple[float, float],
            validator: ConfigValidator,
            value_name: str = "Value"
    ) -> float | tuple[float, float]:
        """
        Validates the `cutoff` parameter.

        Args:
            value (float or tuple of float): The cutoff value(s) to validate.
            validator (ConfigValidator): Validator instance for checking.
            value_name (str): Descriptive name for the value in error messages.

        Returns:
            float or tuple of float: The validated cutoff value(s).

        Raises:
            ValueError: If the value is not a float or a tuple of two floats in the range [0, 100].
        """
        validator.ensure_type(value=value, types=(float, list, tuple), value_name=value_name)
        if isinstance(value, (tuple, list)):
            value = validator.validate_number_tuple(
                value=value,
                value_name=value_name,
                allowed_types=(float,),
                length=2
            )
            return tuple(value)
        value = validator.validate_number(
            value=value,
            value_name=value_name,
            allowed_types=(float,),
            min_value=0,
            max_value=100
        )
        return value

    @staticmethod
    def validate_ignore(
            value: int | Sequence[int],
            validator: ConfigValidator,
            value_name: str = "Value"
    ) -> int | Sequence[int]:
        """
        Validates the `ignore` parameter.

        Args:
            value (int or list/tuple of int): The pixel value(s) to ignore.
            validator (ConfigValidator): Validator instance for checking.
            value_name (str): Descriptive name for the value in error messages.

        Returns:
            int or list/tuple of int: The validated ignore value(s).

        Raises:
            ValueError: If any value is not an int in the range [0, 255].
        """
        validator.ensure_type(value=value, types=(int, list, tuple), value_name=value_name)
        if isinstance(value, (tuple, list)):
            for element in value:
                validator.validate_number(
                    value=element,
                    value_name=value_name,
                    allowed_types=(int,),
                    min_value=0,
                    max_value=255
                )
            return value
        value = validator.validate_number(
            value=value,
            value_name=value_name,
            allowed_types=(int,),
            min_value=0,
            max_value=255
        )
        return value
