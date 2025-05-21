from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transformation_abstract import Transformation


@register_transform
class FlipImage(Transformation):
    """
    Flip an image vertically (top-to-bottom).

    This transform produces a vertical mirror of the input image by
    inverting it along the horizontal axis. No parameters are required.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: "flip"
        """
        return "flip"

    def apply(self, image: Image.Image, params=None) -> Image.Image:
        """
        Perform a vertical flip on the provided image.

        Args:
            image (Image.Image): The source PIL image.
            params (None or dict or list): Must be one of (None, {}, []);
                this transform does not accept parameters.

        Returns:
            Image.Image: A new image flipped vertically.

        Raises:
            TypeError: If `params` is not None or an empty container.
        """
        if params not in (None, {}, []):
            raise TypeError(f"{self.key()} does not accept parameters; got: {params!r}")
        return ImageOps.flip(image)
