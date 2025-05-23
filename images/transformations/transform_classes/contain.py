from PIL import Image, ImageOps

from images.transformations.filters_mapping import RESAMPLING_FILTERS
from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class ContainImage(Transformation):
    """
    Scale an image to fit within the specified size, preserving aspect ratio.

    This transform resizes the image so that it is contained within the
    width and height given, without cropping or distorting the aspect ratio.
    Any empty space is filled with the image’s own background color.
    """
    def key(self) -> str:
        """
        Return the configuration key used to invoke this transformation.

        Returns:
            str: "contain"
        """
        return "contain"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Apply “contain” resizing on the provided image.

        Args:
            image (Image.Image): The source PIL image.
            config (dict):
                size (tuple[int, int]): Target (width, height).
                method (str, optional): Resampling filter name.

        Returns:
            Image.Image: A new image resized to fit within `size`.

        Raises:
            TypeError: If `config` is not a dict, if `size` or `method` types are invalid.
            ValueError: If `size` values are non-positive, or `method` is unsupported.
        """
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)

        validator.validate_required_keys(required=["size"], config_dict=config)

        size: tuple[int, int] = validator.validate_int_tuple(value=config.get("size"), value_name="size", length=2)

        method_key: str = validator.validate_choice(
            value_name="method",
            value=config.get("method", "BICUBIC"),
            options=list(RESAMPLING_FILTERS.keys())
        )

        resample_filter = RESAMPLING_FILTERS[method_key]
        return ImageOps.contain(image, size=size, method=resample_filter)
