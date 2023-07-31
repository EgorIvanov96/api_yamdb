from users.users import User
from rest_framework import permissions
from .serializers import (UserRegistrationSerializer,
                          UserInfoSerializer,
                          MeSerializer,
                          UserTokenSerializer,
                          )
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .permissions import (OwnersAndAdmin,
                          OwnerStaffOrReadOnly,
                          IsAdminOrReadOnly)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken


class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, create = User.objects.get_or_create(
                                                        username=username,
                                                        email=email
                                                        )

        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
                'Confirmation code',
                confirmation_code,
                ['yamdb@email.com'],
                (email, ),
                fail_silently=False
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    """Получение JWT-токена."""

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserInfoViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (OwnersAndAdmin, )
    lookup_field = 'username'
    filterset_fields = ('username')
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        )
    def get_user_info(self, request):
        serializer = UserInfoSerializer(request.user)
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
