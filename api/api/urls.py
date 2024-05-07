from django.urls import path
from escuchamos.api import *
from django.conf import settings
from django.conf.urls.static import static

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
    
    path('user/photo/upload/', UserPhotoUpload.as_view(), name='user-photo-upload'),

    path('country/', CountryIndexAPIView.as_view(), name='country-index'),
    path('country/<int:pk>/', CountryShowAPIView.as_view(), name='country-show'),

    path('status/', StatusIndexAPIView.as_view(), name='status-index'),
    path('status/<int:pk>/', StatusShowAPIView.as_view(), name='status-show'),

    path('category/', CategoryIndexAPIView.as_view(), name='category-index'),
    path('category/create/', CategoryStoreAPIView.as_view(), name='category-create'),
    path('category/<int:pk>/', CategoryShowAPIView.as_view(), name='category-show'),
    path('category/update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('category/delete/<int:pk>/', CategoryDeleteAPIView.as_view(), name='category-delete'),
    path('category/restore/<int:pk>/', CategoryRestoreAPIView.as_view(), name='category-restore'),

    path('unit/', UnitIndexAPIView.as_view(), name='unit-index'),
    path('unit/create/', UnitStoreAPIView.as_view(), name='unit-create'),
    path('unit/<int:pk>/', UnitShowAPIView.as_view(), name='unit-show'),
    path('unit/update/<int:pk>/', UnitUpdateAPIView.as_view(), name='unit-update'),
    path('unit/delete/<int:pk>/', UnitDeleteAPIView.as_view(), name='unit-delete'),
    path('unit/restore/<int:pk>/', UnitRestoreAPIView.as_view(), name='unit-restore'),

    path('type-post/', TypePostIndexAPIView.as_view(), name='type-post-index'),
    path('type-post/create/', TypePostStoreAPIView.as_view(), name='type-post-create'),
    path('type-post/<int:pk>/', TypePostShowAPIView.as_view(), name='type-post-show'),
    path('type-post/update/<int:pk>/', TypePostUpdateAPIView.as_view(), name='type-post-update'),
    path('type-post/delete/<int:pk>/', TypePostDeleteAPIView.as_view(), name='type-post-delete'),
    path('type-post/restore/<int:pk>/', TypePostRestoreAPIView.as_view(), name='type-post-restore'),

    path('order-status/', OrderStatusesIndexAPIView.as_view(), name='order-status-index'),
    path('order-status/create/', OrderStatusesStoreAPIView.as_view(), name='order-status-create'),
    path('order-status/<int:pk>/', OrderStatusesShowAPIView.as_view(), name='order-status-show'),
    path('order-status/update/<int:pk>/', OrderStatusesUpdateAPIView.as_view(), name='order-status-update'),
    path('order-status/delete/<int:pk>/', OrderStatusesDeleteAPIView.as_view(), name='order-status-delete'),
    path('order-status/restore/<int:pk>/', OrderStatusesRestoreAPIView.as_view(), name='order-status-restore'),

    path('gender/', GenderIndexAPIView.as_view(), name='gender-index'),
    path('gender/create/', GenderStoreAPIView.as_view(), name='gender-create'),
    path('gender/<int:pk>/', GenderShowAPIView.as_view(), name='gender-show'),
    path('gender/update/<int:pk>/', GenderUpdateAPIView.as_view(), name='gender-update'),
    path('gender/delete/<int:pk>/', GenderDeleteAPIView.as_view(), name='gender-delete'),
    path('gender/restore/<int:pk>/', GenderRestoreAPIView.as_view(), name='gender-restore'),
    
    path('type-person/', TypePersonIndexAPIView.as_view(), name='type-person-index'),
    path('type-person/create/', TypePersonStoreAPIView.as_view(), name='type-person-create'),
    path('type-person/<int:pk>/', TypePersonShowAPIView.as_view(), name='type-person-show'),
    path('type-person/update/<int:pk>/', TypePersonUpdateAPIView.as_view(), name='type-person-update'),
    path('type-person/delete/<int:pk>/', TypePersonDeleteAPIView.as_view(), name='type-person-delete'),
    path('type-person/restore/<int:pk>/', TypePersonRestoreAPIView.as_view(), name='type-person-restore'),

    path('activity/', GenderIndexAPIView.as_view(), name='activity-index'),
    path('activity/create/', GenderStoreAPIView.as_view(), name='activity-create'),
    path('activity/<int:pk>/', GenderShowAPIView.as_view(), name='activity-show'),
    path('activity/update/<int:pk>/', GenderUpdateAPIView.as_view(), name='activity-update'),
    path('activity/delete/<int:pk>/', GenderDeleteAPIView.as_view(), name='activity-delete'),
    path('activity/restore/<int:pk>/', GenderRestoreAPIView.as_view(), name='gender-restore'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
