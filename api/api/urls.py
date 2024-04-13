from django.urls import path
from escuchamos.api import *

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('verify-email/<str:token>/', UserVerifyAPIView.as_view(), name='verify_email'),
    
    path('users', UserIndexAPIView.as_view(), name='user-list'),
    path('user/<int:pk>', UserShowAPIView.as_view(), name='user-show'),
]
