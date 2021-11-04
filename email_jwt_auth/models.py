from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class UserEmailCode(models.Model):
    username = models.CharField(max_length=64)
    email = models.EmailField()
    code = models.IntegerField()
