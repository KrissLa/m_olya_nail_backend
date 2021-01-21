from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Service
from .serializers import ServiceListSerializer


class ServiceListAPIView(ListAPIView):
    """Список услуг"""
    # permission_classes = (IsAdminUser,)
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceListSerializer


class ServiceRetrieveAPIView(RetrieveAPIView):
    """Информация об услуге"""
    # permission_classes = (IsAdminUser,)
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceListSerializer


