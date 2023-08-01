from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from review.models import Genre
from .serializers import GenreSerializer

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