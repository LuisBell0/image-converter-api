from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation


@register_transform
class MirrorImage(Transformation):
    """
    Mirror an image horizontally (left-to-right).

    This transform creates a horizontal reflection of the input image
    by swapping its left and right sides. No parameters are required.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: "mirror"
        """
        return "mirror"

    def apply(self, image: Image.Image, params=None) -> Image.Image:
        """
        Perform a horizontal mirror on the provided image.

        Args:
            image (Image.Image): The source PIL image.
            params (None or dict or list): Must be one of (None, {}, []);
                this transform does not accept parameters.

        Returns:
            Image.Image: A new image mirrored horizontally.

        Raises:
            TypeError: If `params` is not None or an empty container.
        """
        if params not in (None, {}, []):
            raise TypeError(f"{self.key()} does not accept parameters; got: {params!r}")
        return ImageOps.mirror(image)
