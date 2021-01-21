from rest_framework import serializers
from .models import AvailableDate


class AvailableDateListSerializer(serializers.ModelSerializer):
    """ Список дат """

    class Meta:
        model = AvailableDate
        fields = ("date", )