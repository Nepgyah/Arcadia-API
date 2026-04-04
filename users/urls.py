from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.AdminLoginView.as_view(), name='users-admin-login'),
    path('', views.UserView.as_view(), name='users-user'),
    path('profile/', views.UserDetailView.as_view(), name='users-user-details')
]