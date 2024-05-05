from django.urls import path
from escuchamos.api import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', WelcomeAPIView.as_view(), name=''),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('verification/', EmailVerificationAPIView.as_view(), name='verification'),
    
    path('user/', UserIndexAPIView.as_view(), name='user-list'),
    path('user/create/', UserStoreAPIView.as_view(), name='user-create'),
    path('user/<int:pk>/', UserShowAPIView.as_view(), name='user-show'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('user/restore/<int:pk>/', UserRestoreAPIView.as_view(), name='user-restore'),

    path('country/', CountryIndexAPIView.as_view(), name='country-index'),
    path('country/<int:pk>/', CountryShowAPIView.as_view(), name='country-show'),

    path('status/', StatusIndexAPIView.as_view(), name='status-index'),
    path('status/<int:pk>/', StatusShowAPIView.as_view(), name='status-show'),

    path('category/', CategoryIndexAPIView.as_view(), name='category-index'),
    path('category/create/', CategoryStoreAPIView.as_view(), name='category-store'),
    path('category/<int:pk>/', CategoryShowAPIView.as_view(), name='category-show'),
    path('category/update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('category/delete/<int:pk>/', CategoryDeleteAPIView.as_view(), name='category-delete'),
    path('category/restore/<int:pk>/', CategoryRestoreAPIView.as_view(), name='category-restore'),

    path('unit/', UnitIndexAPIView.as_view(), name='unit-index'),
    path('unit/create/', UnitStoreAPIView.as_view(), name='unit-store'),
    path('unit/<int:pk>/', UnitShowAPIView.as_view(), name='unit-show'),
    path('unit/update/<int:pk>/', UnitUpdateAPIView.as_view(), name='unit-update'),
    path('unit/delete/<int:pk>/', UnitDeleteAPIView.as_view(), name='unit-delete'),
    path('unit/restore/<int:pk>/', UnitRestoreAPIView.as_view(), name='unit-restore'),

    path('type-post/', TypePostIndexAPIView.as_view(), name='type-post-index'),
    path('type-post/create/', TypePostStoreAPIView.as_view(), name='type-post-store'),
    path('type-post/<int:pk>/', TypePostShowAPIView.as_view(), name='type-post-show'),
    path('type-post/update/<int:pk>/', TypePostUpdateAPIView.as_view(), name='type-post-update'),
    path('type-post/delete/<int:pk>/', TypePostDeleteAPIView.as_view(), name='type-post-delete'),
    path('type-post/restore/<int:pk>/', TypePostRestoreAPIView.as_view(), name='type-post-restore'),
]
urlpatterns += staticfiles_urlpatterns()
