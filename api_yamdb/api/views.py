from users.users import User
from rest_framework import permissions
from .serializers import (GenreSerializer,
                          UserRegistrationSerializer,
                          UserSerializer,
                          ProfileSerializer,
                          TokenSerializer,
                          ReviewSerializer,
                          CommentsSerializer,
                          TitlesSerializer,
                          CategorySerializer,
                          )
from review.models import Comments, Review, Titles, Genre, Category
from .permissions import (OwnersAndAdmin,
                          SuperUserOrAdmin)

from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination


class UserRegistrationView(APIView):
    """Регистрация пользователя."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, create = User.objects.get_or_create(username=username,
                                                  email=email)

        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
                'Your Confirmation code',
                user.confirmation_code,
                ['yamdb@mail.com'],
                (email, ),
                fail_silently=False
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Получение JWT-токена."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (SuperUserOrAdmin, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ("get", "post", "patch", "delete")
    pagination_class = PageNumberPagination

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        )
    def get_user_info(self, request):
        serializer = ProfileSerializer(
            request.user, partial=True, data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "PATCH":
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        return Review.objects.filter(titles_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = Titles.objects.get(id=title_id)
        serializer.save(author=self.request.user,
                        titles_id=title)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        return Comments.objects.filter(review=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = Review.objects.get(id=review_id)
        serializer.save(author=self.request.user,
                        review=review)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    #permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
    search_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field = 'slug'
    #pagination_class = PageNumberPagination
    #permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter)
    filterset_fields = ('name', 'titles__slug')
    search_fields = ('name', 'titles__slug')

    def create(self, request, *args, **kwargs):
        # Проверяем, что slug не дублируется
        slug = request.data.get('slug')
        existing_category = Category.objects.filter(slug=slug).first()
        if existing_category:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Категория с таким slug уже существует.'})

        return super().create(request, *args, **kwargs)


class GenereaViewSet(viewsets.ModelViewSet): # Жанры
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #pagination_class = LimitOffsetPagination
    #permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter)
    filterset_fields = ('name', 'titles__slug')
    search_fields = ('name', 'titles__slug')

    def create(self, request, *args, **kwargs):
        # Проверяем, что slug не дублируется
        slug = request.data.get('slug')
        existing_category = Genre.objects.filter(slug=slug).first()
        if existing_category:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Категория с таким slug уже существует.'})

        return super().create(request, *args, **kwargs)
