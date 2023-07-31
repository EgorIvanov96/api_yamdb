from rest_framework import viewsets, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from review.models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet): # Жанры
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_class = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        # Проверяем, что slug не дублируется
        slug = request.data.get('slug')
        existing_category = Category.objects.filter(slug=slug).first()
        if existing_category:
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data={'error': 'Категория с таким slug уже существует.'})

        return super().create(request, *args, **kwargs)