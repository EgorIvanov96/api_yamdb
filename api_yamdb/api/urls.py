from rest_framework import routers
from django.urls import include, path

from api.views import ReviewViewSet


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/review',
    ReviewViewSet,
    basename='review')

urlpatterns = [
    path('v1/', include(router.urls)),
]
