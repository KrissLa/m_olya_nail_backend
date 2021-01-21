from django.contrib import admin
from .models import AvailableDate

# Register your models here.

@admin.register(AvailableDate)
class AvailableDateAdmin(admin.ModelAdmin):
    """Модель дат в админке"""
    pass