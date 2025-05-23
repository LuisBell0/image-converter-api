from PIL import Image, ImageOps

from images.transformations.filters_mapping import RESAMPLING_FILTERS
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


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
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)

        factor: float | int = validator.validate_number(value=config.get("factor"), value_name="factor")

        resample: str = validator.validate_choice(
            value=config.get("resample", "BICUBIC"),
            value_name="resample",
            options=list(RESAMPLING_FILTERS.keys())
        )

        return ImageOps.scale(image=image, factor=factor, resample=RESAMPLING_FILTERS[resample])
