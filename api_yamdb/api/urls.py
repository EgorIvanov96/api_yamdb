from django.urls import path, include
from .views import UserRegistrationView, UserViewSet, TokenView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/token/', TokenView.as_view()),
    path('auth/signup/', UserRegistrationView.as_view()),
    path('', include(router.urls)),
]