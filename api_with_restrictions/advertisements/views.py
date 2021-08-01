from django.shortcuts import redirect
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement
from .serializers import AdvertisementSerializer


def home(request):
    return redirect('api/')


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all().select_related('creator')
    serializer_class = AdvertisementSerializer

    search_fields = ['creator__id']

    filterset_class = AdvertisementFilter

    # вот это аналогично созданию фильтра с таким параметром, но нам нужен "кастомный" по дате
    # filterset_fields = ['created_at']

    # def get_permissions(self):
    #     """Получение прав для действий."""
    #     if self.action in ["create", "update", "partial_update"]:
    #         return [IsAuthenticated()]
    #     return []
