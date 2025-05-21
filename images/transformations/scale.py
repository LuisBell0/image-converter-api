from PIL import Image, ImageOps
from PIL.Image import Resampling

from images.transformations.transformation_abstract import Transformation

RESAMPLING_FILTERS: dict = {
    'NEAREST': Resampling.NEAREST,
    'BOX': Resampling.BOX,
    'BILINEAR': Resampling.BILINEAR,
    'HAMMING': Resampling.HAMMING,
    'BICUBIC': Resampling.BICUBIC,
    'LANCZOS': Resampling.LANCZOS,
}


class ScaleImage(Transformation):
    """
    Scales an image by a given factor using a specified resampling filter.

    Configuration:
        - factor (float): Scale multiplier (e.g. 0.5 to reduce size by half).
        - resample (str): Resampling filter name, one of: NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS.
    """
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        """
        Return the key used in the pipeline configuration dict to invoke this transformation.

        Returns:
            str: "scale"
        """
        return "scale"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Applies the scale transformation to the image.

        Args:
            image (Image.Image): The source image.
            config (dict): Must contain:
                - "factor" (float or int): Scale multiplier.
                - "resample" (str, optional): Name of resampling filter.

        Returns:
            Image.Image: Scaled image.

        Raises:
            TypeError: If inputs are of the wrong type or missing required keys.
        """
        if not isinstance(config, dict):
            raise TypeError(f"{self.key()} configuration must be a valid JSON object")

        factor: float | int = config.get("factor")
        if not factor:
            raise TypeError("factor value must be specified")
        if not isinstance(factor, (int, float)):
            raise TypeError(f"{self.key()} factor must be a valid integer or float")

        resample: str = config.get("resample", "BICUBIC")
        if not isinstance(resample, str):
            raise TypeError("Resample value must be a valid string")
        resample_str: str = resample.upper()
        if resample_str not in RESAMPLING_FILTERS:
            raise TypeError(f"Resample value must be one of {list(RESAMPLING_FILTERS.keys())}")

        return ImageOps.scale(image=image, factor=factor, resample=RESAMPLING_FILTERS[resample_str])
