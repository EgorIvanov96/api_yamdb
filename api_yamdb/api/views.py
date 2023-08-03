from rest_framework import (viewsets, permissions, status, filters, mixins,
                            serializers)
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .permissions import SuperUserOrAdmin, IsUserAdminOrReadOnly

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from review.models import Titles, Category, Genre, Review, Titles
from .serializers import (
    TitlesSerializer, CategorySerializer, GenreSerializer, ReviewSerializer,
    CommentsSerializer, Comments)
from .permissions import SuperUserOrAdmin, OwnerModerAdmin
from .serializers import (
    UserRegistrationSerializer, UserSerializer,
    ProfileSerializer, TokenSerializer,)
from users.users import User


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
        try:
            user = User.objects.get(username=serializer.validated_data['username'])
            confirmation_code = user.confirmation_code
        except User.DoesNotExist:
            return Response(
                {'username': 'Такой пользователь не существует'},
                status=status.HTTP_404_NOT_FOUND)
        if (serializer.validated_data['confirmation_code']
           == confirmation_code):
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Код подтвердения неверный!'},
            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    permission_classes = (SuperUserOrAdmin, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
        serializer = ProfileSerializer(request.user, data=request.data,
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == "PATCH":
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (OwnerModerAdmin,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        return Comments.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = Review.objects.get(id=review_id)
        serializer.save(author=self.request.user,
                        review=review)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    pass
    

class CategoryViewSet(ListCreateDestroyViewSet, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    #permission_class = (IsUserAdminOrReadOnly,)
    permission_classes = (SuperUserOrAdmin,)
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
    
    """def get_permissions(self):
        if self.action == 'get':
            permission_class = (permissions.IsAuthenticatedOrReadOnly,)
        else:
            permission_class = (permissions.IsAdminUser,)
        return [permission() for permission in permission_class]"""


class GenereaViewSet(ListCreateDestroyViewSet, viewsets.GenericViewSet): # Жанры
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerModerAdmin,)
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


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    #permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
    search_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerModerAdmin,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        return Review.objects.filter(titles=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = Titles.objects.get(id=title_id)
        author = self.request.user
        review_exists = Review.objects.filter(
            author=author, titles=title).exists()
        if review_exists:
            raise serializers.ValidationError(
                {'error': 'Можно оставить только один отзыв'})
        serializer.save(author=author, titles=title)
