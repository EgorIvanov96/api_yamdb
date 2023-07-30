from django.shortcuts import render
from users.users import User
from rest_framework import permissions
from django.core.mail import send_mail
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers


class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user = User.objects.get_or_create()
            default_token_generator.make_token(user)
            return send_mail(f'Token - {token}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

