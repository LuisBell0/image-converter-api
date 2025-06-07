from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from .models import ImageConversion


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageConversion
        fields = ['id', 'user', 'converted_image', 'conversion_format']
        read_only_fields = ['created_at', 'updated_at']


class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField(allow_empty_file=False)

    def validate_image(self, image: InMemoryUploadedFile):
        max_size = 5 * 1024 * 1024  # e.g. 5 MB

        if image.size > max_size:
            raise serializers.ValidationError(
                f"The uploaded image is too heavy. Max size: {max_size // (1024*1024)}MB, got {image.size // (1024*1024)}MB"
            )

        buffered = BytesIO(image.read())
        try:
            pil_img = Image.open(buffered)
            pil_img.verify()
        except Exception:
            raise serializers.ValidationError("Uploaded file is not a valid image.")

        buffered.seek(0)
        image_format = pil_img.format.upper()
        allowed_formats = ["JPEG", "PNG", "WEBP"]
        if image_format not in allowed_formats:
            raise serializers.ValidationError({
                "detail": f"Unsupported image format: {image_format}. Must be one of {list(allowed_formats)}."
            })

        image.seek(0)
        return image
