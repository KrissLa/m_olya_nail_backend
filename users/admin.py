from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    """Модель пользователя в админке"""
    list_display = ('id', "name", "telegram_id", "is_banned", )
    list_display_links = ('id', 'name', "telegram_id",)
    readonly_fields = ('id', 'name', 'telegram_id', 'username', 'personal_cashback_level', 'referral_cashback_level',
                       'created_at',)
    list_filter = ('is_banned', 'created_at',)
    search_fields = ("id", "name", "username", 'phone_number', 'referer__name')

    fieldsets = (
        (None, {
            'fields': (
                ('id',),
                ('telegram_id',),
                ('name', 'username'),
                ('phone_number',),
                ('personal_cashback_level', 'referral_cashback_level'),
                ('created_at',),
                ('bonus_balance', 'frozen_balance'),
                ('is_banned',),
                ('referer',),
            )
        }),

    )


@admin.register(BonusTransaction)
class BonusTransactionAdmin(admin.ModelAdmin):
    """Модель бонусных транзакций в админке"""
    list_display = ('id', "user", "type", "amount", "comment", 'created_at')
    list_display_links = ('id', 'user', "type", "amount", "comment", 'created_at')
    readonly_fields = ('id', 'user', "type", "amount", "comment", 'created_at')
    list_filter = ('type', 'comment', 'created_at')
    search_fields = ("id", "user__name", "type", "amount", "comment")

