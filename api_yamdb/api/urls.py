from django.urls import path, include

urlpatterns = [
    path('auth/signup/', include('djoser.urls')),
    path('auth/token/', include('djoser.urls')),
    path('users/', include('djoser.urls')),
]