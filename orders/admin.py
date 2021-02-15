from django.contrib import admin
from django.contrib.admin import StackedInline

from .models import Order, Discount, OrderRating


# Register your models here.


# @admin.register(Discount)
# class DiscountAdmin(admin.ModelAdmin):
#     """ Модель скидок в админке """
#     list_display = ("order", "type", "discount_amount", "discount_amount_BYN")
#     list_display_links = ("order", "type", "discount_amount", "discount_amount_BYN")
#     readonly_fields = ("order", "type", "discount_amount", "discount_amount_BYN")
#     list_filter = ("type",)
#     search_fields = ("order__id", "type", "order__user__name")


@admin.register(OrderRating)
class OrderRatingAdmin(admin.ModelAdmin):
    """ Модель скидок в админке """
    list_display = ("order", "rating", "review",)
    list_display_links = ("order", "rating", "review",)
    readonly_fields = ("order", "rating", "review",)
    list_filter = ("rating", "rating_viewed", "review_viewed")
    search_fields = ("rating", "review", "order__user__name")


class DiscountAdminInline(StackedInline):
    """ Модель скидок в админке """
    model = Discount
    extra = 0
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class OrderRatingAdminInline(StackedInline):
    """ Модель отзывов в админке """
    model = OrderRating
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Модель заказа в админке"""
    list_display = ('id', 'user', 'service_date', 'service_name', 'total_price', "status")
    list_display_links = ('id', 'user', 'service_date', 'service_name', 'total_price', "status")
    readonly_fields = ('id', 'user', 'service_date', 'date', 'service_name', 'service_price', 'service_time',
                       'total_price', 'bonus_points', 'status', 'is_user_notified', 'reason_for_reject')
    list_filter = ('service_name', 'status', "service_date__date")
    search_fields = ("id", "service_name", "user__name", 'reason_for_reject')
    inlines = [DiscountAdminInline, OrderRatingAdminInline]
