from django.urls import path
from escuchamos.api import *

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('verify-email/<str:token>/', UserVerifyAPIView.as_view(), name='verify_email'),
    
    path('users', UserIndexAPIView.as_view(), name='user-list'),
    path('user/create', UserStoreAPIView.as_view(), name='user-create'),
    path('user/<int:pk>', UserShowAPIView.as_view(), name='user-show'),
    path('user/update/<int:pk>', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/delete/<int:pk>', UserDeleteAPIView.as_view(), name='user-delete'),
    path('user/restore/<int:pk>', UserRestoreAPIView.as_view(), name='user-restore'),

    path('countries', CountryIndexAPIView.as_view(), name='country-index'),
    path('country/<int:pk>', CountryShowAPIView.as_view(), name='country-show'),
]
