from django.shortcuts import render
from users.users import User
from rest_framework import permissions
from django.core.mail import send_mail
from .serializers import UserRegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegisterView(APIView):
    def post(self, request):
        serializer_class = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get_or_create()
            default_token_generator.make_token(user)
            return send_mail(f'Token - {token}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

