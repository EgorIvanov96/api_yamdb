from django.urls import path, include
from .views import UserRegisterView

urlpatterns = [
    path('auth/token/', token_post),
    path('auth/signup/', signup_post),
]