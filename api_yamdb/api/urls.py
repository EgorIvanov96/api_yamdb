from django.urls import path, include
from .views import UserRegistrationView, UserInfoViewSet, APIGetToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserInfoViewSet)

urlpatterns = [
    path('auth/token/', APIGetToken.as_view()),
    path('auth/signup/', UserRegistrationView.as_view()),
    path('', include(router.urls)),
]