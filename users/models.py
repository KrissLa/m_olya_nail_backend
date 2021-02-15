from django.db import models


class BotUser(models.Model):
    """Модель пользователей в бд"""
    telegram_id = models.BigIntegerField("Telegram ID", unique=True)
    name = models.CharField("Имя пользователя", max_length=150, blank=True, default='')
    username = models.CharField("Никнейм в телеграме", max_length=200, blank=True, default='')
    phone_number = models.CharField("Номер телефона", max_length=13, blank=True, default='')
    personal_cashback_level = models.PositiveSmallIntegerField("Уровень персонального кэшбэка", default=1)
    referral_cashback_level = models.PositiveSmallIntegerField("Уровень реферального кэшбэка", default=0)
    is_banned = models.BooleanField("Блокировка", default=False)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    bonus_balance = models.PositiveBigIntegerField("Бонусный баланс", default=0)
    frozen_balance = models.PositiveIntegerField("Замороженный бонусный баланс", default=0)
    referer = models.ForeignKey("BotUser", verbose_name="Пригласивший", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.id}. {self.name}'


class BonusTransaction(models.Model):
    """ Модель бонусных транзакций в бд """
    TRANSACTION_TYPE_CHOICES = (
        ("reward", "Зачисление"),
        ("write_off", "Списание"),
    )

    user = models.ForeignKey(BotUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    type = models.CharField("Тип операции", max_length=9, choices=TRANSACTION_TYPE_CHOICES)
    created_at = models.DateTimeField("Дата транзакции", auto_now_add=True)
    amount = models.PositiveIntegerField("Количество бонусных баллов", default=0)
    comment = models.CharField("Комментарий", max_length=150, blank=True)

    class Meta:
        verbose_name = "Операция с бонусным балансом"
        verbose_name_plural = "Операции с бонусным балансом"

    def __str__(self):
        return f'{self.user}. {self.type} - {self.amount}'
