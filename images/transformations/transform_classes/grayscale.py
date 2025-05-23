from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation


@register_transform
class GrayscaleImage(Transformation):
    """
    Convert an image to grayscale.

    This transform converts an RGB or multi-band image into its
    luminance equivalent, discarding color information. No parameters
    are required.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: "grayscale"
        """
        return "grayscale"

    def apply(self, image: Image.Image, params=None) -> Image.Image:
        """
        Perform a grayscale conversion on the provided image.

        Args:
            image (Image.Image): The source PIL image.
            params (None or dict or list): Must be one of (None, {}, []);
                this transform does not accept parameters.

        Returns:
            Image.Image: A new image in grayscale ("L" mode).

        Raises:
            TypeError: If `params` is not None or an empty container.
        """
        if params not in (None, {}, []):
            raise TypeError(f"{self.key()} does not accept parameters; got: {params!r}")
        return ImageOps.grayscale(image)
