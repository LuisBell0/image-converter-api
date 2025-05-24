from PIL import Image

from images.transformations.filters_mapping import RESAMPLING_FILTERS
from images.transformations.registry import register_transform
from images.transformations.transform_classes.transformation_abstract import Transformation
from images.transformations.validators import ConfigValidator


@register_transform
class ThumbnailImage(Transformation):
    def __init__(self):
        super().__init__()

    def key(self) -> str:
        return "thumbnail"

    def apply(self, image: Image.Image, config: dict) -> Image.Image:
        validator = ConfigValidator(key=self.key())
        config = validator.validate_dictionary(config_dict=config)
        validator.validate_required_keys(config_dict=config, required=["size"])

        size: tuple[float, float] = validator.validate_number_tuple(
            value=config.get("size"),
            value_name="size",
            allowed_types=(float,),
            length=2
        )
        resample: str = validator.validate_choice(
            value=config.get("resample", "BICUBIC"),
            value_name="resample",
            options=list(RESAMPLING_FILTERS.keys())
        )
        reducing_gap: float | None = validator.validate_number(
            value=config.get("reducing_gap", 2.0),
            value_name="reducing_gap",
            allowed_types=(float,)
        )

        image.thumbnail(size=size, resample=RESAMPLING_FILTERS[resample], reducing_gap=reducing_gap)

        return image
