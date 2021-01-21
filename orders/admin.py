from django.contrib import admin
from .models import Order, Discount


# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Модель """
    pass

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Модель"""
    pass