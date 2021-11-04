from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import EmailTokenAuthAPI, UserEmailCodeLoginAPI


urlpatterns = [
    path('signup/', EmailTokenAuthAPI.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', UserEmailCodeLoginAPI.as_view())
]