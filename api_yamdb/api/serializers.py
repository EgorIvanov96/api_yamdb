from rest_framework import serializers
from users.users import User
from django.contrib.auth.validators import UnicodeUsernameValidator

class UserRegisterSerializer(serializers.Serializer):
    validator = UnicodeUsernameValidator()
    def validate(self, attrs):
        pass