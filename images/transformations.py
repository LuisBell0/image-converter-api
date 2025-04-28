from .models import FORMAT_CHOICES


def convert_image_format(image, new_format):
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


def resize_image(image, config):
    width = config.get("width")
    height = config.get("height")

    try:
        width = int(width) if width is not None else image.width
        height = int(height) if height is not None else image.height
    except (TypeError, ValueError):
        raise ValueError("Width and height must be valid integers.")

    return image.resize((width, height))
