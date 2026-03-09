from django.urls import path
from . import views

urlpatterns = [
    # path('demo/login/', views.DemoLoginView.as_view(), name='users_demo_login'),
    path('', views.UserView.as_view(), name='user'),
    path('<int:id>/', views.UpdateUser.as_view(), name='users_update_user' )
]