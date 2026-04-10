from django.urls import path
from . import endpoints

urlpatterns = [
    path('admin-login/', endpoints.AdminLoginView.as_view(), name='auth-admin-login'),
    path('refresh/', endpoints.RefreshTokenView.as_view(), name='auth-refresh'),
]