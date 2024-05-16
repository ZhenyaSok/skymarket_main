from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .filters import AdFilter
from .models import Ad, Comment
from .permissions import IsAdminOrOwner
from .serializers import AdDetailSerializer, AdSerializer, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    """Пагинация для объявлений"""
    page_size = 4
    page_query_param = "page"


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter
    pagination_class = AdPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdDetailSerializer
        return AdSerializer

    def get_permissions(self):
        """Создавать и просматривать может любой авторизованный пользователь, а редактировать
        и удалять только владелец или админ"""
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        if self.action in ['create', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании объекта"""
        new_ad = serializer.save()
        new_ad.author = self.request.user
        new_ad.save()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Получает отзывы для определенного объявления"""
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, id=ad_id)
        return ad.reviews.all().order_by("created_at")

    def get_permissions(self):
        """Создавать и просматривать может любой авторизованный пользователь, а редактировать
        и удалять только владелец или админ"""
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
            # permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwner]
            # permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца отзыва в определенном объявлении"""
        new_review = serializer.save()
        new_review.author = self.request.user
        new_review.ad = Ad.objects.get(pk=self.kwargs["ad_pk"])
        new_review.save()


class MyListAPIView(generics.ListAPIView):
    """Возвращает список объявлений текущего пользователя"""

    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AdPagination

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)

