from rest_framework import serializers
from .models import Service


class ServiceListSerializer(serializers.ModelSerializer):
    """ Список вопросов """

    class Meta:
        model = Service
        fields = "__all__"