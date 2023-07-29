from rest_framework import routers
from django.urls import include, path

from api.views import CommentViewSet


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/review/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
