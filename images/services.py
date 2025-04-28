import json
import os
from io import BytesIO

from rest_framework import status
from rest_framework.response import Response


def _save_conversion(image, original_name, original_format, config):
    """Saves the image conversion for authenticated users."""
    buffer = BytesIO()

    new_format = config.get("format", original_format)
    quality = config.get("optimize", 100)

    format_str = new_format.upper()
    extension = new_format.lower()

    image.save(buffer, format=format_str, quality=quality, optimize=True)
    buffer.seek(0)

    filename_base, _ = os.path.splitext(original_name)
    new_filename = f"{filename_base}.{extension}"

    return new_filename, buffer, format_str


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
