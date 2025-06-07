import json
import os
from io import BytesIO
from typing import Any, Dict, Tuple

from PIL import Image
from django.core.files.base import ContentFile
from django.http import FileResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from accounts_jwt.models import CustomUser
from images.models import ImageConversion


def respond_anonymous(buffer: BytesIO, filename: str) -> FileResponse:
    """
    Returns a FileResponse for the given buffer, with the specified filename.

    The buffer is rewound to the beginning before being returned as a downloadable file.

    Args:
        buffer: An in-memory file-like object containing the data to serve.
        filename: The name of the file to present in the download response.

    Returns:
        FileResponse: A Django response that prompts the user to download the file.
    """
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)


def save_authenticated(user: CustomUser, buffer: BytesIO, filename: str, conversion_format: str) -> ImageConversion:
    """
    Persist an image from memory and record its conversion.

    Rewinds the buffer, wraps its bytes in a Django ContentFile, and:
      1. Creates an ImageConversion record with status 'completed'.
      2. Saves the ContentFile to the record’s `converted_image` field.

    Args:
        user: The owner of the new ImageConversion.
        buffer: In-memory image data.
        filename: Filename under which to store the image.
        conversion_format: Target format (e.g. 'png', 'jpeg').

    Returns:
        The saved ImageConversion instance with the image attached.
    """
    file_content = ContentFile(buffer.getvalue(), name=filename)
    conversion = ImageConversion.objects.create(
        user=user, conversion_format=conversion_format)
    conversion.converted_image.save(filename, file_content, save=True)
    return conversion


def save_conversion(image: Image.Image,
                     original_name: str,
                     original_format: str,
                     config: Dict[str, Any]) -> Tuple[str, BytesIO, str]:
    """
    Apply format/quality conversions to an image and return the result.

    The image is saved into a new in-memory buffer using options from `config`.
    If `config` does not specify a new format or quality,
    the original format is retained with default quality.

    Args:
        image: A PIL image to convert.
        original_name: Filename of the source image (e.g. 'photo.png').
        original_format: Format of the source image (e.g. 'png', 'jpeg').
        config: Conversion options:
            - 'format' (str): target format, e.g. 'png' or 'jpeg'.
            - 'optimize' (int): quality level 1–100 (default: 100).

    Returns:
        A tuple of:
        1. `new_filename` (str): e.g. 'photo.jpeg'
        2. `buffer` (BytesIO): contains the converted image bytes.
        3. `output_format_str` (str): uppercase format name used for saving (e.g. 'JPEG').
    """
    buffer = BytesIO()

    new_format = config.get("format", original_format)
    quality = config.get("optimize", 100)

    output_format_str = new_format.upper()
    output_extension = new_format.lower()

    image.save(buffer, format=output_format_str, quality=quality, optimize=True)
    buffer.seek(0)

    filename_base, _ = os.path.splitext(original_name)
    new_filename = f"{filename_base}.{output_extension}"

    return new_filename, buffer, output_format_str


def parse_config(request: Request) -> Dict[str, Any] | Response:
    """
    Extract and validate a JSON configuration payload from the request.

    Attempts to read `config` from POST data, parse it as JSON, and ensure it’s
    an object. Returns the parsed dict on success or an appropriate Response
    with HTTP 400 on failure.

    Args:
        request: DRF Request carrying POST data.

    Returns:
        Dict[str, Any]: The parsed configuration dictionary.
        Response: A DRF Response with error details and HTTP 400 status.
    """
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
