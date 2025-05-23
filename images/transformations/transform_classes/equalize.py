from PIL import Image, ImageOps

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation


@register_transform
class EqualizeImage(Transformation):
    """
    Apply histogram equalization to an image to enhance contrast.

    This transform does not take any parameters—if it’s in your pipeline,
    it always runs.  To include it in the pipeline, set its config value to
    null (None) or an empty dict.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: "equalize"
        """
        return "equalize"

    def apply(self, image: Image.Image, params=None) -> Image.Image:
        """
        Perform histogram equalization on the provided image.

        Args:
            image (Image.Image): The source PIL image.
            params (None or dict or list): Must be one of (None, {}, []);
                this transform does not accept parameters.

        Returns:
            Image.Image: A new image with equalized histogram.

        Raises:
            TypeError: If `params` is not None or an empty container.
        """
        if params not in (None, {}, []):
            raise TypeError(f"{self.key()} does not accept parameters; got: {params!r}")
        return ImageOps.equalize(image)
