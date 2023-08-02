from rest_framework import viewsets, permissions, status, filters
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from review.models import Titles, Category, Genre
from .serializers import TitlesSerializer, CategorySerializer, GenreSerializer

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    permission_class = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
    search_fields = ('category', 'genre', 'name', 'year')
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_class = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')

    def create(self, request, *args, **kwargs):
        # Проверяем, что slug не дублируется
        slug = request.data.get('slug')
        existing_category = Category.objects.filter(slug=slug).first()
        if existing_category:
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data={'error': 'Категория с таким slug уже существует.'})

        return super().create(request, *args, **kwargs)
    

class GenereaViewSet(viewsets.ModelViewSet): # Жанры
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_class = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')

    def create(self, request, *args, **kwargs):
        # Проверяем, что slug не дублируется
        slug = request.data.get('slug')
        existing_category = Genre.objects.filter(slug=slug).first()
        if existing_category:
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data={'error': 'Категория с таким slug уже существует.'})

        return super().create(request, *args, **kwargs)