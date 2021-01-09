from rest_framework import serializers
from .models import Picture


class PicturesListSerializer(serializers.ModelSerializer):
    """ Список пользователей """

    class Meta:
        model = Picture
        fields = "__all__"


