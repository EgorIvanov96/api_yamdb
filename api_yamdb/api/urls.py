from rest_framework import routers
from django.urls import path, include

from .views import *
from .views import UserRegistrationView, UserViewSet, TokenView
from api.views import ReviewViewSet

from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/review',
    ReviewViewSet,
    basename='review')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenereaViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/token/', TokenView.as_view()),
    path('auth/signup/', UserRegistrationView.as_view()),

