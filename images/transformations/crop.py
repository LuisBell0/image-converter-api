from PIL import Image

from images.transformations.registry import register_transform
from images.transformations.transformation_abstract import Transformation


@register_transform
class CropImage(Transformation):
    """
    Transformation that crops a PIL Image based on provided bounding box coordinates.

    Missing values in the config default to the image edges.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: The config key, "crop".
        """
        return "crop"

    def apply(self, image: Image, config: dict) -> Image:
        """
        Crop the input image according to the given configuration.

        Args:
            image (Image.Image): The source PIL Image to transform.
            config (dict): Dictionary containing crop parameters:
                - left (int or str, optional): The left x-coordinate.
                - upper (int or str, optional): The upper y-coordinate.
                - right (int or str, optional): The right x-coordinate.
                - lower (int or str, optional): The lower y-coordinate.

        Returns:
            Image.Image: The cropped image.

        Raises:
            ValueError: If any coordinate cannot be converted to an integer,
                        or if the resulting box is invalid or out of bounds.
        """
        if not isinstance(config, dict):
            raise ValueError("Crop configuration must be a JSON object")

        img_width, img_height = image.size
        left = config.get("left")
        right = config.get("right")
        upper = config.get("upper")
        lower = config.get("lower")

        try:
            left = int(left) if left is not None else 0
            right = int(right) if right is not None else img_width
            upper = int(upper) if upper is not None else 0
            lower = int(lower) if lower is not None else img_height
        except (TypeError, ValueError):
            raise ValueError("Crop coordinates must be valid integers.")

        if not (0 <= left < right <= img_width and 0 <= upper < lower <= img_height):
            raise ValueError("Invalid crop box: "
                             f"expected 0 ≤ left({left}) < right({right}) ≤ width({img_width}), "
                             f"0 ≤ upper({upper}) < lower({lower}) ≤ height({img_height})")

        return image.crop((left, upper, right, lower))
