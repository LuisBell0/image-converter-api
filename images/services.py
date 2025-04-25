import json
import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response

from .models import ImageConversion


def convert_image(image_file, new_format=None, quality_percentage=100):
    """
    Converts the image to a specified format, optimizes it, and returns:
    (ContentFile, new_filename, format_str)
    """
    img = Image.open(image_file)
    original_format = img.format
    image_format = new_format or original_format
    image_format = image_format.lower()
    buffer = BytesIO()

    if image_format == "jpeg" or image_format == "jpg":
        extension = "jpg"
        img = img.convert("RGB")
        img.save(buffer, format="JPEG", quality=quality_percentage, optimize=True, progressive=True)
    elif image_format == "png":
        extension = "png"
        img.save(buffer, format="PNG", optimize=True)
    elif image_format == "webp":
        extension = "webp"
        img = img.convert("RGB") if img.mode in ("RGBA", "P") else img
        img.save(buffer, format="WEBP", quality=quality_percentage, method=6)
    else:
        raise ValueError(f"Unsupported format: {image_format}")

    filename_base, _ = os.path.splitext(os.path.basename(image_file.name))
    new_filename = f"{filename_base}.{extension}"

    return ContentFile(buffer.getvalue()), new_filename, extension.upper()


def resize_image(image_file, width=None, height=None):
    buffer = BytesIO()
    image = Image.open(image_file)

    try:
        width = int(width) if width is not None else image.width
        height = int(height) if height is not None else image.height
    except (TypeError, ValueError):
        return Response({"detail": "Width and height must be valid integers."}, status=status.HTTP_400_BAD_REQUEST)

    image_resized = image.resize((width, height))
    image_resized.save(buffer, format=image.format)

    filename_base, _ = os.path.splitext(os.path.basename(image_file.name))
    new_filename = f"{filename_base}.{image.format.lower()}"
    return ContentFile(buffer.getvalue()), new_filename


def _save_conversion(self, user, filename, format_str, content):
    """Saves the image conversion for authenticated users."""
    conversion = ImageConversion.objects.create(
        user=user,
        conversion_format=format_str,
        status='completed'
    )
    conversion.converted_image.save(filename, content, save=True)
    return conversion


def _parse_config(self, request):
    """Parses and validates the config JSON."""
    raw_config = request.POST.get("config")
    if not raw_config:
        return Response({"detail": "Missing 'config' in POST data."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        config = json.loads(raw_config)
    except json.JSONDecodeError:
        return Response({"detail": "Invalid JSON format in 'config'."}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(config, dict):
        return Response({"detail": "'config' must be a JSON object."}, status=status.HTTP_400_BAD_REQUEST)

    return config
