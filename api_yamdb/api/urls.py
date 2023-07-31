from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
]