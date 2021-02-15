from datetime import timedelta

from django.db import models
from loguru import logger

from users.models import BotUser
from available_dates.models import AvailableDate


# Create your models here.


class Order(models.Model):
    """Модель заказа в бд"""
    STATUS_CHOICES = (
        ("wait", "Оформлен, Ожидает завершения"),
        ("completed", "Завершен"),
        ("canceled", "Отменен"),
    )

    user = models.ForeignKey(BotUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    service_date = models.ForeignKey(AvailableDate, verbose_name="Дата и время", on_delete=models.CASCADE)
    date = models.DateTimeField("Дата заказа", auto_now_add=True)
    service_name = models.CharField("Название услуги", max_length=255)
    service_price = models.DecimalField("Полная стоимость услуги", max_digits=4, decimal_places=2)
    service_time = models.CharField("Время выполнения", max_length=25, default="")
    total_price = models.DecimalField("Итоговая стоимость услуги", max_digits=4, decimal_places=2)
    bonus_points = models.PositiveIntegerField("Будет начислено бонусных баллов", default=0)
    status = models.CharField("Статус заказа", max_length=9, choices=STATUS_CHOICES, default="wait")
    is_user_notified = models.BooleanField("Напоминание пользователю отправлено", default=False)
    reason_for_reject = models.TextField("Причина отмены заказа", null=True, blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.id}. {self.service_name}, {self.service_date}'


class Discount(models.Model):
    """Модель скидок в заказе"""
    SALES_TYPE_CHOICES = (
        ("percent", "Акционная скидка"),
        ("points", "Бонусная скидка"),
    )
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name="discounts")
    type = models.CharField("Тип скидки", max_length=7, choices=SALES_TYPE_CHOICES)
    discount_amount = models.PositiveIntegerField("Значение скидки в % или ББ")
    discount_amount_BYN = models.DecimalField("Значение скидки в BYN", max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Скидка в заказе"
        verbose_name_plural = "Скидки в заказе"

    def __str__(self):
        if self.type == "percent":
            name = "Акционная скидка"
            value = "%"
        else:
            name = "Бонусная скидка"
            value = "ББ"
        return f"{name}: {self.discount_amount} {value}. ({self.discount_amount_BYN} BYN)"


class OrderRating(models.Model):
    """ Модель оценок в заказе """
    order = models.OneToOneField(Order, verbose_name="Заказ", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField("Оценка")
    review = models.TextField("Отзыв", null=True, blank=True)
    rating_viewed = models.BooleanField("Оценка просмотрена", default=False)
    review_viewed = models.BooleanField("Отзыв просмотрен", default=True)

    class Meta:
        verbose_name = "Отзыв к заказу"
        verbose_name_plural = "Отзывы к заказу"

    def __str__(self):
        return f'Заказ № {self.order.id}, Оценка: {self.rating}'
