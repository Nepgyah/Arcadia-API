from django.urls import path
from . import endpoints

urlpatterns = [
    path('admin/login/', endpoints.adminLoginView, name="account_admin_login"),
    path('tokens/refresh/', endpoints.refreshTokenView, name="account_token_refresh")
]