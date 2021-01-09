from rest_framework import serializers
from .models import Question


class QuestionListSerializer(serializers.ModelSerializer):
    """ Список вопросов """

    class Meta:
        model = Question
        fields = "__all__"