from PIL import Image

from images.transformations.filters_mapping import BASIC_FILTERS, RANK_FILTERS, MULTIBAND_FILTERS
from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class BasicImageFilter(Transformation):
    """
    Applies one or more basic PIL image filters in sequence.

    Supported filters are defined in BASIC_FILTERS. Filters can be applied
    individually or as a list for chaining effects.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The config key, "basic_filter".
        """
        return "basic_filter"

    def apply(self, image: Image.Image, image_filter: str | list[str]) -> Image.Image:
        """
        Apply one or more PIL basic filters to an image.

        Args:
            image (Image.Image):
                The source image to transform.
            image_filter (str or list of str):
                - If a single string, apply that filter.
                - If a list of strings, apply each filter in sequence.

        Returns:
            Image.Image: The filtered image.

        Raises:
            TypeError:
                - If `image_filter` is None or empty.
                - If `image_filter` is not a `str` or `list` of `str`.
                - If any element of the list is not a string.
            ValueError:
                If any filter name is not one of the supported keys.
        """
        validator = ConfigValidator(key=self.key())
        filters: list[str] = validator.validate_str(
            value=image_filter,
            value_name="image_filter",
            allowed=list(BASIC_FILTERS.keys()),
            multiple=True
        )

        for validated_fiter in filters:
            image = image.filter(BASIC_FILTERS[validated_fiter])

        return image


@register_transform
class RankImageFilter(Transformation):
    """
    Transformation that applies a rank-based PIL filter (Min, Max, Median)
    with a specified window size.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key "rank_filter".
        """
        return "rank_filter"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Apply a rank filter to the given image using parameters from config.

        Args:
            image (Image.Image): The source image to transform.
            config (dict): Configuration object containing:
                - size (int): positive integer window size for the filter.
                - filter_name (str): name of the rank filter to apply.

        Returns:
            Image.Image: The filtered image.

        Raises:
            TypeError: If config is not a dict, if 'size' is not a positive int,
                       or if 'filter_name' is not a string.
            ValueError: If required keys are missing or filter_name is invalid.
        """
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)
        validator.validate_required_keys(config_dict=config, required=["size"])

        size: int = validator.validate_number(value=config.get("size"), value_name="size", allowed_types=(int,))

        method_name: str = validator.validate_choice(
            value=config.get("filter_name"),
            options=list(RANK_FILTERS.keys()),
            value_name="filter_name",
        )
        return image.filter(RANK_FILTERS[method_name](size=size))


@register_transform
class MultibandImageFilter(Transformation):
    """
    Transformation that applies a multiband PIL filter (e.g., GaussianBlur, UnsharpMask)
    with a specified radius parameter.

    The configuration must be a dict with:
        - radius (int): positive radius value for the filter.
        - filter_name (str): name of the multiband filter (e.g., 'GAUSSIANBLUR', 'UNSHARPMASK').

    Registered under the key 'multiband_filter'.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The key "multiband_filter".
        """
        return "multiband_filter"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Apply a multiband filter to the given image using parameters from config.

        Args:
            image (Image.Image): The source image to transform.
            config (dict): Configuration object containing:
                - 'radius' (int): positive integer radius for the filter.
                - 'filter_name' (str): name of the multiband filter to apply.

        Returns:
            Image.Image: The filtered image.

        Raises:
            TypeError: If config is not a dict, if 'radius' is not a positive int,
                       or if 'filter_name' is not a string.
            ValueError: If required keys are missing or filter_name is invalid.
        """
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)

        radius: int = validator.validate_number(value=config.get("radius"), value_name="radius", min_value=1)

        method_name: str = validator.validate_choice(
            value=config.get("filter_name"),
            options=list(MULTIBAND_FILTERS.keys()),
            value_name="filter_name"
        )

        return image.filter(MULTIBAND_FILTERS[method_name](radius=radius))
