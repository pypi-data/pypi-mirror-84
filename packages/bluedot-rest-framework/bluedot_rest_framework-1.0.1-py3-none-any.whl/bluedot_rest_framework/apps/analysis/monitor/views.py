from project.utils.viewsets import CustomModelViewSet
from rest_framework.response import Response
from .models import Monitor
from .serializers import MonitorSerializer


class MonitorView(CustomModelViewSet):
    model_class = Monitor
    serializer_class = MonitorSerializer
    permission_classes = []
