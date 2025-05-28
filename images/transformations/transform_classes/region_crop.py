from PIL import Image

from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class CropImageRegion(Transformation):
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
            str: The config key, "region_crop".
        """
        return "region_crop"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        """
        Crop the input image according to the given configuration.

        Args:
            image (Image.Image): The source PIL Image to transform.
            config (dict): Dictionary containing crop parameters:
                - left (int): The left x-coordinate.
                - upper (int): The upper y-coordinate.
                - right (int): The right x-coordinate.
                - lower (int): The lower y-coordinate.

        Returns:
            Image.Image: The cropped image.

        Raises:
            TypeError: If config is not a dictionary.
            ValueError: If any coordinate cannot be converted to an integer,
                        or if the resulting box is invalid or out of bounds.
        """
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)

        img_width, img_height = image.size
        left: int = config.get("left", 0)
        right: int = config.get("right", img_width)
        upper: int = config.get("upper", 0)
        lower: int = config.get("lower", img_height)

        left, upper, right, lower = self.validate_crop_box(
            left=left,
            upper=upper,
            right=right,
            lower=lower,
            img_width=img_width,
            img_height=img_height,
            validator=validator
        )

        return image.crop(box=(left, upper, right, lower))

    @staticmethod
    def validate_crop_box(
        left: int, upper: int, right: int, lower: int,
        img_width: int,
        img_height: int,
        validator: ConfigValidator
    ) -> tuple[int, int, int, int]:
        """
        Validates cropping box coordinates against image dimensions.

        Ensures that the provided crop box coordinates (`left`, `upper`, `right`, `lower`)
        are integers and form a valid rectangle within the bounds of the image.

        Args:
            left (int): The left x-coordinate.
            upper (int): The upper y-coordinate.
            right (int): The right x-coordinate.
            lower (int): The lower y-coordinate.
            img_width (int): The image width.
            img_height (int): The image height.
            validator (ConfigValidator): Validator instance for checking.

        Returns:
            tuple[int, int, int, int]: The validated crop box as a tuple (left, upper, right, lower).

        Raises:
            TypeError: If any coordinate is not an integer.
            ValueError: If the crop box coordinates are not within the image bounds or do not form a valid box.
        """
        for name, coord in (("left", left), ("upper", upper),
                            ("right", right), ("lower", lower)):
            validator.ensure_type(value=coord, types=(int,), value_name=name)
        if not (0 <= left < right <= img_width):
            raise ValueError(
                f"{validator.key} invalid horizontal crop coords: "
                f"0 ≤ left({left}) < right({right}) ≤ width({img_width})"
            )
        if not (0 <= upper < lower <= img_height):
            raise ValueError(
                f"{validator.key} invalid vertical crop coords: "
                f"0 ≤ upper({upper}) < lower({lower}) ≤ height({img_height})"
            )
        return left, upper, right, lower
