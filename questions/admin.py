from django.contrib import admin
from .models import Question

# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Модель вопросов в админке"""
    list_display = ('id', 'user', 'is_answered', 'created_at', 'question')
    list_display_links = ('id', 'user', 'is_answered', 'created_at', 'question')
    readonly_fields = ('id', 'user', 'question', 'answer', 'answered_at', 'is_answered', 'created_at', 'answer_time')
    list_filter = ('is_answered', 'created_at', )
    search_fields = ("id", "question", "user__name")
