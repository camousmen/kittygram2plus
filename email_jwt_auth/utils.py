import jwt
from datetime import datetime, timedelta
from django.conf import settings

from kittygram2plus.settings import SECRET_KEY


def generate_access_token(user):
    """
    Генерирует веб-токен JSON, в котором хранится идентификатор, срок действия
    потом возьмем с настроек проекта, по умолчанию 1 день от создания
    """

    dt = datetime.utcnow() + timedelta(days=1)
    access_token_payload = {
        'id': user.pk,
        'exp': dt
    }
    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY, algorithm='HS256'
    )
    print(jwt.decode(access_token, settings.SECRET_KEY, algorithms='HS256'))
    return access_token