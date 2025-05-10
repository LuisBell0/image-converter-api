from PIL import Image

from images.transformations.transformation_abstract import Transformation


class ResizeImage(Transformation):
    """
    Transformation that resizes a PIL Image based on provided width and/or height.

    If only one dimension is provided, the other defaults to the image's original size.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transform.

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
                - width (int or str, optional): Target width in pixels.
                - height (int or str, optional): Target height in pixels.

        Returns:
            Image.Image: The resized image.

        Raises:
            ValueError: If width or height cannot be converted to an integer.
        """
        if not isinstance(config, dict):
            raise ValueError("resize must be a JSON object")

        width = config.get("width") or None
        height = config.get("height") or None

        try:
            width = int(width) if width is not None else image.width
            height = int(height) if height is not None else image.height
        except (TypeError, ValueError):
            raise ValueError("Width and height must be valid integers.")

        return image.resize((width, height))
