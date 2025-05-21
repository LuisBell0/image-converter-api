from PIL import Image

from images.transformations.registry import register_transform
from images.transformations.transformation_abstract import Transformation


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
        if not isinstance(config, dict):
            raise TypeError(f"{self.key()} configuration must be a JSON object")

        angle: int | float = config.get("angle")
        expand: bool = config.get("expand", False)
        fill_color: str | None = config.get("fillcolor", None)

        if angle is None or not isinstance(angle, (int, float)):
            raise ValueError("Angle must be provided as an integer or float.")
        if not isinstance(expand, bool):
            raise ValueError("Expand must be boolean if provided.")
        if fill_color is not None and not isinstance(fill_color, str):
            raise ValueError("FillColor must be a string if provided.")

        rotate_args: dict = {"angle": angle, "expand": expand}
        if fill_color:
            from PIL import ImageColor
            rotate_args["fillcolor"] = ImageColor.getcolor(color=fill_color, mode='RGB')

        return image.rotate(**rotate_args)
