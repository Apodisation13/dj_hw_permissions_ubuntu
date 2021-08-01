from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement
from .permissions import IsAuthOrReadOnly, IsOwner
from .serializers import AdvertisementSerializer


def home(request):
    return redirect('api/')


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all().select_related('creator')  # SELECT_RELATED
    serializer_class = AdvertisementSerializer

    search_fields = ['creator__id']

    filterset_class = AdvertisementFilter

    # вот это аналогично созданию фильтра с таким параметром, но нам нужен "кастомный" по дате
    # filterset_fields = ['created_at']

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsOwner()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return []
