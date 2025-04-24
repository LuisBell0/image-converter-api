from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwner
from .serializers import ImageSerializer
from .models import ImageConversion
from .services import optimize_image


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

        content, filename, format_str = optimize_image(image_file)
        conversion = ImageConversion.objects.create(
            user=request.user,
            conversion_format=format_str,
            status='completed'
        )

        conversion.converted_image.save(filename, content, save=True)

        serializer = self.get_serializer(conversion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
