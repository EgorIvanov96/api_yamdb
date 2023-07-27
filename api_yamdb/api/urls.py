from django.urls import path, include
from .views import UserRegisterView

urlpatterns = [
    path('auth/signup/', UserRegisterView.as_view()),
    path('auth/token/', UserRegisterView.as_view()),
    path('users/', UserRegisterView.as_view()),
]