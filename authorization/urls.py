from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.AdminLoginView.as_view(), name='auth-admin-login'),
    path('refresh/', views.RefreshTokenView.as_view(), name='auth-refresh'),
]