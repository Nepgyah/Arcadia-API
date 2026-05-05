from django.urls import path
from . import endpoints

urlpatterns = [
    path('export-list/', endpoints.export_list, name='asobu-export-list')
]