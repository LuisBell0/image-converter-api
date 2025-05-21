from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transformation_abstract import Transformation


@register_transform
class InvertImage(Transformation):
    """
    Invert an image’s colors.

    This transform produces a photographic negative by mapping each pixel
    value to 255 − original. Only works on “L”, “RGB”, or multi-band images.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: "invert"
        """
        return "invert"

    def apply(self, image: Image.Image, params=None) -> Image.Image:
        """
        Perform color inversion on the provided image.

        Args:
            image (Image.Image): The source PIL image.
            params (None or dict or list): Must be one of (None, {}, []);
                this transform does not accept parameters.

        Returns:
            Image.Image: A new image with inverted colors.

        Raises:
            TypeError: If `params` is not None or an empty container.
        """
        if params not in (None, {}, []):
            raise TypeError(f"{self.key()} does not accept parameters; got: {params!r}")
        return ImageOps.invert(image)
