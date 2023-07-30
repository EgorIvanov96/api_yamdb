from django.urls import path, include
from .views import UserRegistrationView

urlpatterns = [
    # path('auth/token/', token_post),
    path('auth/signup/', UserRegistrationView.as_view()),
]