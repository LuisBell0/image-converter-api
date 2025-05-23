from abc import ABC, abstractmethod

from PIL import Image


class Transformation(ABC):
    """Base class for image transformations.

    Subclasses must implement `.key()` to identify themselves in a config
    dict, and `.apply()` to perform the actual image operation.

    Methods:
        key:     Return the config key (e.g. "resize", "format", etc.).
        apply:   Perform the transformation on a PIL Image.
    """

    @abstractmethod
    def key(self) -> str:
        """Return the config key under which this transformation is registered.

        Returns:
            str: The name used in the pipeline config to invoke this transform.
        """
        ...

    @abstractmethod
    def apply(self, image: Image.Image, params) -> Image.Image:
        """Apply this transformation to the given image.

        Args:
            image (Image.Image): The source image to transform.
            params (any):       Configuration parameters for this transform.

        Returns:
            Image.Image: The transformed image.

        Raises:
            ValueError: If `params` is invalid (e.g. missing keys, bad types).
        """
        ...
