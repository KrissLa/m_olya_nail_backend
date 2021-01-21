from django.db import models


class Service(models.Model):
    """ Таблица с услугами """
    name = models.CharField("Название услуги", max_length=250)
    price = models.PositiveIntegerField("Стоимость услуги (BYN)")
    time = models.CharField("Время выполнения (с указание ед. измерения)", max_length=25)
    discount = models.BooleanField("Включить скидку", default=False)
    discount_amount = models.PositiveIntegerField("Размер скидки в (%)", default=10)
    is_active = models.BooleanField("Доступна", default=True)


    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        if self.discount:
            return f"{self.name} - {self.price} BYN (ДЕЙСТВУЕТ СКИДКА {self.discount_amount}%)"
        else:
            return f"{self.name} - {self.price} BYN"
