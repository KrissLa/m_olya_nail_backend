from django.db import models

# Create your models here.


class Picture(models.Model):
    """Фотографии из инстаграма"""

    photo_url = models.URLField("Ссылка на оригинальную фотографию", max_length=500, unique=True)
    added_at = models.DateTimeField("Время добавления", auto_now_add=True)
    draft = models.BooleanField("Скрыть", default=False)

    class Meta:
        verbose_name = "Фотография из инстаграма"
        verbose_name_plural = "Фотографии из инстаграма"

    def __str__(self):
        return f"{self.id}, {self.added_at.strftime('%d.%m.%Y')}"