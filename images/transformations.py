from PIL import Image

from .models import FORMAT_CHOICES


def convert_image_format(image: Image.Image, new_format: str) -> Image.Image:
    """
    Converts the image to a specified format.
    """
    if type(new_format) is not str:
        raise TypeError("Format must be a string")
    valid_formats = {format for format, _ in FORMAT_CHOICES}
    if new_format.upper() not in valid_formats:
        allowed_formats = ', '.join(valid_formats)
        raise ValueError(f'Format must be one of the following formats: {allowed_formats}')
    if not new_format:
        return image
    return image.convert("RGB") if new_format.lower() in ["jpeg", "jpg", "webp"] else image


def resize_image(image: Image.Image, config: dict) -> Image.Image:
    width = config.get("width")
    height = config.get("height")

    try:
        width = int(width) if width is not None else image.width
        height = int(height) if height is not None else image.height
    except (TypeError, ValueError):
        raise ValueError("Width and height must be valid integers.")

    return image.resize((width, height))


def crop_image(image: Image.Image, config: dict) -> Image.Image:
    """
    Crops `image` according to config dict with keys:
      - left, upper, right, lower (all optional; integers)

    Missing values default to the image edge.
    """
    img_width, img_height = image.size
    left = config.get("left")
    right = config.get("right")
    upper = config.get("upper")
    lower = config.get("lower")

    try:
        left = int(left) if left is not None else 0
        right = int(right) if right is not None else img_width
        upper = int(upper) if upper is not None else 0
        lower = int(lower) if lower is not None else img_height
    except (TypeError, ValueError):
        raise ValueError("Crop coordinates must be valid integers.")

    if not (0 <= left < right <= img_width and 0 <= upper < lower <= img_height):
        raise ValueError("Invalid crop box: "
                         f"expected 0 ≤ left({left}) < right({right}) ≤ width({img_width}), "
                         f"0 ≤ upper({upper}) < lower({lower}) ≤ height({img_height})")

    return image.crop((left, upper, right, lower))
