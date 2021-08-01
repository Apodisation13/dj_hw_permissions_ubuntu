from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement
from .permissions import IsOwnerOrIsAdmin
from .serializers import AdvertisementSerializer


def home(request):
    return redirect('api/')


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all().select_related('creator')
    serializer_class = AdvertisementSerializer

    search_fields = ['creator__id', 'status']

    filterset_class = AdvertisementFilter

    # вот это аналогично созданию фильтра с таким параметром, но нам нужен "кастомный" по дате
    # filterset_fields = ['created_at']

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsOwnerOrIsAdmin()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        if self.request.user.is_authenticated:
            q1 = Advertisement.objects.exclude(status='DRAFT').select_related('creator')
            q2 = Advertisement.objects.filter(creator__id=self.request.user.id, status='DRAFT').select_related('creator')
            queryset = q1 | q2
        else:
            queryset = Advertisement.objects.filter(status__in=['OPEN', 'CLOSED']).select_related('creator')
        return queryset
