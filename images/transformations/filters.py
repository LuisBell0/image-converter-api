from PIL import Image, ImageFilter

from images.transformations.registry import register_transform
from images.transformations.transformation_abstract import Transformation

BASIC_FILTERS: dict = {
    'BLUR': ImageFilter.BLUR,
    'CONTOUR': ImageFilter.CONTOUR,
    'DETAIL': ImageFilter.DETAIL,
    'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
    'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
    'EMBOSS': ImageFilter.EMBOSS,
    'FIND_EDGES': ImageFilter.FIND_EDGES,
    'SHARPEN': ImageFilter.SHARPEN,
    'SMOOTH': ImageFilter.SMOOTH,
    'SMOOTH_MORE': ImageFilter.SMOOTH_MORE,
}

RANK_FILTERS: dict = {
    'MIN': ImageFilter.MinFilter,
    'MEDIAN': ImageFilter.MedianFilter,
    'MAX': ImageFilter.MaxFilter,
}

MULTIBAND_FILTERS: dict = {
    'UNSHARPMASK': ImageFilter.UnsharpMask,
    'GAUSSIANBLUR': ImageFilter.GaussianBlur,
    'BOXBLUR': ImageFilter.BoxBlur,
}


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
        if not image_filter:
            raise TypeError(f"{self.key()} value must be provided as a string or list of strings")

        if isinstance(image_filter, str):
            filters: list[str] = [image_filter]
        elif isinstance(image_filter, list):
            if not all(isinstance(f, str) for f in image_filter):
                raise TypeError(f"All {self.key()}'s must be strings")
            filters: list[str] = image_filter
        else:
            raise TypeError(f"{self.key()} must be a string or a list of strings")

        for f in filters:
            if f not in BASIC_FILTERS:
                raise ValueError(f"Unknown basic filter '{f}', must be one of: {list(BASIC_FILTERS.keys())}")
            image = image.filter(BASIC_FILTERS[f])

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
                - 'size' (int): positive integer window size for the filter.
                - 'filter_name' (str): name of the rank filter to apply.

        Returns:
            Image.Image: The filtered image.

        Raises:
            TypeError: If config is not a dict, if 'size' is not a positive int,
                       or if 'filter_name' is not a string.
            ValueError: If required keys are missing or filter_name is invalid.
        """
        if not isinstance(config, dict):
            raise TypeError(f"{self.key()} configuration must be a valid JSON object.")

        size: int = config.get("size")
        if size is None:
            raise ValueError(f"{self.key()} missing required field 'size'.")
        if not isinstance(size, int) or size <= 0:
            raise TypeError(f"{self.key()} 'size' must be a positive integer.")

        name: str = config.get("filter_name")
        if name is None:
            raise ValueError(f"{self.key()} missing required field 'filter_name'.")
        if not isinstance(name, str):
            raise TypeError(f"{self.key()} 'name' must be a string.")
        filter_name: str = name.upper()
        if filter_name not in RANK_FILTERS:
            raise ValueError(f"Unknown {self.key()} '{filter_name}'. Must be one of: {list(RANK_FILTERS.keys())}")

        return image.filter(RANK_FILTERS[filter_name](size=size))


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
        if not isinstance(config, dict):
            raise TypeError(f"{self.key()} configuration must be a valid JSON object.")

        radius: int = config.get("radius")
        if radius is None:
            raise ValueError(f"{self.key()} missing required field 'radius'.")
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise TypeError(f"{self.key()} 'radius' must be a positive integer.")

        name: str = config.get("filter_name")
        if name is None:
            raise ValueError(f"{self.key()} missing required field 'filter_name'.")
        if not isinstance(name, str):
            raise TypeError(f"{self.key()} 'name' must be a string.")
        filter_name: str = name.upper()
        if filter_name not in MULTIBAND_FILTERS:
            raise ValueError(
                f"Unknown {self.key()} '{filter_name}'. Must be one of: {list(MULTIBAND_FILTERS.keys())}"
            )

        return image.filter(MULTIBAND_FILTERS[filter_name](radius=radius))
