from rest_framework import serializers
from .models import ImageConversion


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageConversion
        fields = ['id', 'user', 'converted_image', 'conversion_format']
        read_only_fields = ['status', 'created_at', 'updated_at']
