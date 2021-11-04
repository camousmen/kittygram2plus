from rest_framework import viewsets
from rest_framework import filters
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .permissions import OwnerOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle
from .pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly, )
    # Если кастомный тротлинг-класс вернет True - запросы будут обработаны
    # Если он вернет False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    # А далее применится лимит low_request
    throttle_scope = 'low_request'
    # подключаем наш собственный класс пагинации с page_size=20
    pagination_class = None
    # указываем фильтрующие бекенды DjangoFilterBackend, поиск, сортировку
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    # фильтровать будем по полям color и birth_year модели Cat
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name', 'owner__username') # поля для поиска
    ordering_fields = ('name', 'birth_year') # поля для сортировки


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        # если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            return (ReadOnly(), )
        # для остальных текущий пермишен
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer