from django.urls import path, include
from .views import CategoryViewSet, UserRegistrationView, UserViewSet, TokenView, CommentViewSet, ReviewViewSet, TitlesViewSet, GenereaViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserViewSet)
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenereaViewSet, basename='genres')
router.register(
    r'titles/(?P<id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('auth/token/', TokenView.as_view()),
    path('auth/signup/', UserRegistrationView.as_view()),
    path('', include(router.urls)),
]
