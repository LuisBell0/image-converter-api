from PIL import Image

from .transformations.registry import TRANSFORM_MAP


def process_image_pipeline(image_file: Image, config: dict) -> tuple[Image.Image, str]:
    """
    Process an image through a sequence of registered transformations.

    Opens the given image file, records its original format, and applies each
    transformation found in the global TRANSFORM_MAP according to the provided
    configuration.

    Args:
        image_file: A file path or file-like object representing the input image.
        config (dict): Mapping of transformation keys (str) to their parameter values.

    Returns:
        tuple[Image.Image, str]:
            - The processed PIL Image.
            - The image's original format as a string.

    Raises:
        KeyError: If a transformation key in `config` is not present in TRANSFORM_MAP.
        ValueError: If a transformation's `apply` method raises an error for invalid params.
    """
    img = Image.open(image_file)
    original_format = img.format

    for key, params in config.items():
        transformer = TRANSFORM_MAP.get(key)
        if transformer:
            img = transformer.apply(img, params)

    return img, original_format
