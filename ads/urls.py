from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .apps import AdsConfig
from .views import AdViewSet, CommentViewSet, MyListAPIView



app_name = AdsConfig.name

router = SimpleRouter()
router.register(r'ads', AdViewSet, basename='ads')
# router.register(r'comment_list', CommentViewSet, basename='comment_list')
router.register(r'ads/(?P<ad_pk>\d+)/comments', CommentViewSet, basename='comment')



urlpatterns = [
    path("", include(router.urls)),
    path('me/', MyListAPIView.as_view(), name='user_ad')
]
