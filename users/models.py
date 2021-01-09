from django.db import models


# Create your models here.

class PersonalCashback(models.Model):
    """Таблица со значениями персонального кэшбэка"""
    level = models.PositiveSmallIntegerField("Уровень", unique=True, primary_key=True)
    value = models.DecimalField("Значение в процентах", max_digits=2, decimal_places=1, unique=True)
    min_order_quantity = models.PositiveIntegerField("Минимальное количество заказов", unique=True)
    max_order_quantity = models.PositiveIntegerField("Максимальное количество заказов", unique=True)

    class Meta:
        verbose_name = "Уровень персонального кэшбэка"
        verbose_name_plural = "Уровни персонального кэшбэка"

    def __str__(self):
        return f"Уровень {self.pk} - {self.value}% ({self.min_order_quantity} - {self.max_order_quantity})"


class ReferalCashback(models.Model):
    """Таблица со значениями реферального кэшбэка"""
    level = models.PositiveSmallIntegerField("Уровень", unique=True, primary_key=True)
    value = models.DecimalField("Значение в процентах", max_digits=2, decimal_places=1, unique=True)
    min_ref_order_quantity = models.PositiveIntegerField("Минимальное количество заказов рефералов", unique=True)
    max_ref_order_quantity = models.PositiveIntegerField("Максимальное количество заказов рефералов", unique=True)

    class Meta:
        verbose_name = "Уровень реферального кэшбэка"
        verbose_name_plural = "Уровни реферального кэшбэка"

    def __str__(self):
        return f"Уровень {self.pk} - {self.value}% ({self.min_ref_order_quantity} - {self.max_ref_order_quantity})"


class BotUser(models.Model):
    """Модель пользователей в бд"""
    telegram_id = models.BigIntegerField("Telegram ID", unique=True)
    name = models.CharField("Имя пользователя", max_length=150, blank=True, default='')
    username = models.CharField("Никнейм в телеграме", max_length=200, blank=True, default='')
    phone_number = models.CharField("Номер телефона", max_length=13, blank=True, default='')
    is_banned = models.BooleanField("Блокировка", default=False)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    can_be_invited = models.BooleanField("Может быть рефералом?", default=True)
    bonus_balance = models.PositiveBigIntegerField("Бонусный баланс", default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} - {self.telegram_id}'


class BotUserCashback(models.Model):
    """Уровень кэшбэка пользователя"""
    user = models.OneToOneField(BotUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    personal_cashback = models.ForeignKey(PersonalCashback, verbose_name="Уровень персонального кэшбэка",
                                          related_name='personal_cashback', on_delete=models.SET_NULL, null=True)
    referal_cashback = models.ForeignKey(ReferalCashback, verbose_name="Уровень реферального кэшбэка",
                                         related_name='referal_cashback', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Кэшбэк пользователя"
        verbose_name_plural = "Кэшбэк пользователей"

    def __str__(self):
        return f"{self.user}"


class Referal(models.Model):
    """Модель рефералов в бд"""
    referer = models.ForeignKey(BotUser, verbose_name="Пригласивший", on_delete=models.CASCADE,
                                related_name='referer')
    referal = models.ForeignKey(BotUser, verbose_name="Приглашенный", on_delete=models.CASCADE,
                                related_name='referal')

    class Meta:
        verbose_name = "Приглашенный пользователь"
        verbose_name_plural = "Приглашенные пользователи"

    def __str__(self):
        return f'{self.referer} - {self.referal}'
