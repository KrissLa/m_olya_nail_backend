import pytz
from django.db import models


class AvailableDate(models.Model):
    """ Модель таблицы с доступными датами """
    date = models.DateTimeField("Дата и время", unique=True)
    is_available = models.BooleanField("Свободная дата", default=True)

    class Meta:
        verbose_name = 'Дата и время'
        verbose_name_plural = 'Даты и время'

    def __str__(self):
        return f'{self.date.astimezone(pytz.timezone("Europe/Minsk")).strftime("%d.%m.%Y %H:%M")}'
