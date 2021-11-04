from django.urls import path

from .views import EmailTokenAuthAPI, UserEmailCodeLoginAPI


urlpatterns = [
    path('signup/', EmailTokenAuthAPI.as_view()),
    path('token/', UserEmailCodeLoginAPI.as_view())
]