from rest_framework import serializers
from users.users import User
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserRegistrationSerializer(serializers.Serializer):
    """Регистрация пользователя."""

    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использование username "me" запрещено!')

        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError('Пользователь с таким username уже существует.')

        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        return data


class UserTokenSerializer(serializers.Serializer):
    """Получение токена пользователя."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )