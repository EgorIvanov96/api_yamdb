from users.users import User
from rest_framework import permissions
from .serializers import (UserRegistrationSerializer,
                          UserSerializer,
                          ProfileSerializer,
                          TokenSerializer,)
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .permissions import SuperUserOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken


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
                {'username': 'Такой пользователь не существует.'},
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
