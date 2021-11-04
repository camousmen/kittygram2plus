from django.contrib.auth import authenticate, get_user_model
from django.db.models import fields
from rest_framework import serializers

from .models import UserEmailCode
from .utils import generate_access_token

User = get_user_model()


class  UserRegistrationsSerializer(serializers.ModelSerializer):
    """Для регистрации или получения кода на почту"""

    class Meta:
        model = User
        fields = ['email', 'username']


class UserEmailCodeSerializer(serializers.ModelSerializer):
    """Для получения токена при отправке username и code"""

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = UserEmailCode
        fields = ['username', 'code', 'token']

    def validate(self, data):
        username = data.get('username', None)
        code = data.get('code', None)

        if username is None:
            raise serializers.ValidationError(
                'Нет username'
            )
        if code is None:
            raise serializers.ValidationError(
                'Нет code'
            )
        user = User.objects.get(username=username)
        if user is None:
            raise serializers.ValidationError(
                'Пользователя с таким username нет'
            )

        #if UserEmailCode.objects.filter(username=user.username, code=code, email=user.email):
            # должны выдать ему токен
            #pass

        token = generate_access_token(user=user)
        data['token'] = token
        return data