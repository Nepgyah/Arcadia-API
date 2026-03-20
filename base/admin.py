from django.contrib import admin
from .forms import FranciseForm
from .models import (
    Franchise,
    Genre
)

admin.site.register(Genre)

@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    form = FranciseForm