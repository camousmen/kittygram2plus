from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import jwt
from django.conf import settings

from .models import UserEmailCode
from .serializers import UserEmailCodeSerializer, UserRegistrationsSerializer

User = get_user_model()


class EmailTokenAuthAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        username = serializer.initial_data['username']
        email = serializer.initial_data['email']
        print(User.objects.filter(username=username, email=email))
        if User.objects.filter(username=username, email=email):
            # отправить код без создания юзера
            print("Есть с таким ником и почтой, отправляем код")
            return Response(status.HTTP_400_BAD_REQUEST) # такой пользователь уже есть
        elif User.objects.filter(username=username):
            print("Уже есть с таким ником")
            return Response(status.HTTP_403_FORBIDDEN) # такой пользователь уже есть
        elif User.objects.filter(email=email):
            print("Уже есть с такой почтой")
            pass # на эту почту зареган другой юзер
        # А если свободный ник, свободная почта создаем пользователя и отправляем код
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserEmailCodeLoginAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class =  UserEmailCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)