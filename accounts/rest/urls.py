from django.urls import path
from .endpoints import adminLoginView, refreshTokenView

urlpatterns = [
    path('admin/login/', adminLoginView, name="account_admin_login"),
    path('tokens/refresh/', refreshTokenView, name="account_token_refresh")
]