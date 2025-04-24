import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

from .models import FORMAT_CHOICES


def optimize_image(image_field, quality_percentage=80):
    """
    Optimizes the given image_field and returns (ContentFile, new_filename, format).
    """

    img = Image.open(image_field)
    buffer = BytesIO()
    print(img.format)
    if img.format.lower() == "jpeg":
        extension = "jpeg"
        img = img.convert('RGB')
        img.save(buffer, format="JPEG", quality=quality_percentage, optimize=True, progressive=True)
    elif img.format.lower() == "png":
        extension = 'png'
        img.save(buffer, format="PNG", optimize=True)
    else:
        extension = 'webp'
        img = img.convert('RGB') if img.mode in ("RGBA", "P") else img
        img.save(buffer, format="WEBP", quality=quality_percentage, method=6)

    filename_base, _ = os.path.splitext(os.path.basename(image_field.name))
    new_filename = f"{filename_base}.{extension}"

    return ContentFile(buffer.getvalue()), new_filename, extension.upper()


def convert_image_format(image_path, output_format):
    """
    Converts an image to a specified format.
    """
    if output_format not in dict(FORMAT_CHOICES):
        raise ValueError(f"Format '{output_format}' is not supported.")

    try:
        img = Image.open(image_path)

        file_name, ext = os.path.splitext(os.path.basename(image_path))

        output_path = f"{file_name}.{output_format.lower()}"

        img.save(output_path, output_format)
        print(f"Image successfully converted and saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
