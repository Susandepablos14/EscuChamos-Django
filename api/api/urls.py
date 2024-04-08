from django.urls import path
from escuchamos.api import *

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('verify-email/<str:token>/', UserVerifyAPIView.as_view(), name='verify_email'),
]
