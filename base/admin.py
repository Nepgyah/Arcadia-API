from django.contrib import admin
from .models import (
    Franchise,
    Genre
)
admin.site.register(Franchise)
admin.site.register(Genre)