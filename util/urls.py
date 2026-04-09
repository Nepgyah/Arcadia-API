from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.CSRFTokenView.as_view(), name='get_csrf'),
    path('health-check/', views.HealthCheckView.as_view(), name='health-check')
]