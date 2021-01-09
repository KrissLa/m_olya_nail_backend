from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    """Модель пользователя в админке"""
    pass


@admin.register(Referal)
class ReferalAdmin(admin.ModelAdmin):
    """Модель рефералов в админке"""
    pass


@admin.register(PersonalCashback)
class PersonalCashbackAdmin(admin.ModelAdmin):
    """Модель уровней персонального кэшбэка в админке"""
    pass


@admin.register(ReferalCashback)
class ReferalCashbackAdmin(admin.ModelAdmin):
    """Модель уровней реферального кэшбэка в админке"""
    pass


@admin.register(BotUserCashback)
class BotUserCashbackAdmin(admin.ModelAdmin):
    """Модель кэшбэка пользователей в админке"""
    pass

