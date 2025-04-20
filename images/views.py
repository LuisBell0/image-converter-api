from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwner
from .serializers import ImageSerializer
from .models import ImageConversion


class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageConversion.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = ImageConversion.objects.filter(user=request.user)
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)
