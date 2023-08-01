from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register(r'titles', TitlesViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
]