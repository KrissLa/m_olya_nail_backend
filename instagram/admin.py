from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Picture


@admin.register(Picture)
class PicturesAdmin(admin.ModelAdmin):
    """Модель фотографий из инстаграма в админке"""
    list_display = ('id', "draft", 'get_photography_image_min')
    list_display_links = ('id', )
    list_editable = ('draft', )

    def get_photography_image_min(self, obj):
        return mark_safe(f'<img src={obj.photo_url} width="80">')

    get_photography_image_min.short_description = 'Фотография'
