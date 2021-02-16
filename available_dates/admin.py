from django.contrib import admin
from django.contrib.admin import StackedInline
from django.utils.safestring import mark_safe

from olya_nail.settings import HOST, ADMIN_ADDRESS
from orders.models import Order
from .models import AvailableDate

# Register your models here.


class OrderAdminInline(StackedInline):
    """Модель заказа в админке"""
    model = Order
    fieldsets = (
        (None, {
            'fields': (('id', ),
                       ('user',),
                       ('go_to_order',),)
        }),


    )
    readonly_fields = ('go_to_order', )

    can_delete = False

    def go_to_order(self, obj):
        return mark_safe(f'<a href="{HOST}{ADMIN_ADDRESS}/orders/order/{obj.id}/change/">Перейти к заказу</a>')

    go_to_order.short_description = 'Ссылка на подробную информацию о заказе'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(AvailableDate)
class AvailableDateAdmin(admin.ModelAdmin):
    """Модель дат в админке"""
    list_display = ("date", "is_available")
    list_display_links = ("date", "is_available")
    list_filter = ("date", "is_available")
    inlines = [OrderAdminInline]
