from django.urls import path
from . import endpoints

urlpatterns = [
    path('csrf/', endpoints.ObtainCSRFToken.as_view(), name='util-rest-csrf'),
    path('health-check/', endpoints.health_check, name='util-rest-csrf'),
]