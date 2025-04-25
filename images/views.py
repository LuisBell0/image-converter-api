from io import BytesIO

from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import ImageConversion
from .permissions import IsOwner
from .serializers import ImageSerializer
from .services import convert_image, _save_conversion, _parse_config, resize_image


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageConversion.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = ImageConversion.objects.filter(user=request.user)
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get("converted_image")
        if not image_file:
            raise ValidationError({"converted_image": "No image file was provided."})

        content, filename, format_str = convert_image(image_file)
        conversion = _save_conversion(
            self, user=request.user, content=content, filename=filename, format_str=format_str
        )

        serializer = self.get_serializer(conversion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='convert', permission_classes=[AllowAny])
    def convert_image(self, request):
        config = _parse_config(self, request)
        if isinstance(config, Response):
            return config

        image = request.FILES.get("image")
        if not image:
            return Response({"detail": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        content, filename, format_str = convert_image(
            image_file=image, new_format=config["format"], quality_percentage=config["optimize"]
        )

        if not request.user.is_authenticated:
            return FileResponse(BytesIO(content.read()), as_attachment=True, filename=filename)

        conversion = _save_conversion(
            self, user=request.user, content=content, filename=filename, format_str=format_str
        )
        serializer = self.get_serializer(conversion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='resize', permission_classes=[AllowAny])
    def resize_image_view(self, request):
        config = _parse_config(self, request)
        if isinstance(config, Response):
            return config

        image = request.FILES.get("image")
        if not image:
            return Response({"detail": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        width = config["width"] if "width" in config else None
        height = config["height"] if "height" in config else None
        if width or height:
            result = resize_image(image, width=width, height=height)
            if isinstance(result, Response):
                return result

            content, new_filename = result
            return FileResponse(BytesIO(content.read()), as_attachment=True, filename=new_filename)

        return Response({"detail": "No width or height was provided"}, status=status.HTTP_400_BAD_REQUEST)
