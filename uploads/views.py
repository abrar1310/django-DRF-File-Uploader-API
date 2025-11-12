from rest_framework import viewsets, permissions
from .models import Upload
from .serializers import UploadSerializer

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by('-created_at')
    serializer_class = UploadSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
