from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageSerializer
from .models import ImageConversion


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageConversion.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [IsAuthenticated]
