from django.db import models
from users.models import BotUser


class Question(models.Model):
    """Таблица с вопросами пользователей"""
    user = models.ForeignKey(BotUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    question = models.TextField("Вопрос пользователя")
    answer = models.TextField("Ответ на вопрос", blank=True, null=True)
    is_answered = models.BooleanField("С ответом", default=False)
    created_at = models.DateTimeField("Вопрос задан", auto_now_add=True)
    answered_at = models.DateTimeField("Получен ответ на вопрос в", blank=True, null=True)
    answer_time = models.PositiveBigIntegerField("Время ответа в секундах", blank=True, null=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f'{self.user} - {self.id}'





