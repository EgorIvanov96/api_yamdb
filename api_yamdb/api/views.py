from rest_framework import viewsets, permissions, status, filters
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from review.models import Titles
from .serializers import TitlesSerializer

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    permission_class = (permissions.IsAdminUser,)
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filterset_fields = ('name', 'slug')
    # search_fields = ('name', 'slug')

    """def create(self, request, *args, **kwargs):
        # Проверяем, что slug не дублируется
        slug = request.data.get('slug')
        existing_category = Titles.objects.filter(slug=slug).first()
        if existing_category:
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data={'error': 'Категория с таким slug уже существует.'})

        return super().create(request, *args, **kwargs)"""