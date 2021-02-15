from django.contrib import admin
from .models import Service


# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Модель услуги в админке"""
    list_display = ('id', 'name', 'discount', 'discount_amount', 'is_active')
    list_display_links = ('id', 'name',)
    save_on_top = True
    list_editable = ('discount', 'is_active', 'discount_amount')
    fieldsets = (
        (None, {
            'fields': (
                ('price',),
                ('time',),
                ('is_active',),
            )
        }),
        ('Скидка', {
            'fields': (
                ('discount',),
                ('discount_amount',),
            )
        }),

    )
