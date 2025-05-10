from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import ImageConversion
from .permissions import IsOwner
from .pipeline import process_image_pipeline
from .serializers import ImageSerializer
from .services import _save_conversion, _parse_config, _save_authenticated, _respond_anonymous


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageConversion.objects.all()
    serializer_class = ImageSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), IsOwner()]

    def list(self, request, *args, **kwargs):
        queryset = ImageConversion.objects.filter(user=request.user)
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        config = _parse_config(request)
        if isinstance(config, Response):
            return config

        image = request.FILES.get("image")
        if not image:
            return Response({"detail": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            processed_image, original_format = process_image_pipeline(image, config)
        except (ValueError, TypeError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        new_filename, buffer, new_format = _save_conversion(processed_image, image.name, original_format, config)

        if not request.user.is_authenticated:
            return _respond_anonymous(buffer, new_filename)

        conversion = _save_authenticated(
            user=request.user,
            buffer=buffer,
            conversion_format=original_format,
            filename=new_filename)
        serializer = self.get_serializer(conversion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
