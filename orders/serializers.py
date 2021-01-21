from rest_framework import serializers
# from .models import Service
#
#
# class ServiceListSerializer(serializers.ModelSerializer):
#     """ Список вопросов """
#
#     class Meta:
#         model = Service
#         fields = "__all__"


class OrderDataSerializer(serializers.Serializer):
    """"""
    telegram_id = serializers.IntegerField()
    service_date_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=4, decimal_places=2)
    service_price = serializers.IntegerField()
    discount = serializers.BooleanField()
    discount_amount = serializers.IntegerField()
    discount_amount_BYN = serializers.DecimalField(max_digits=4, decimal_places=2)
    bonus_discount = serializers.BooleanField()
    bonus_discount_amount = serializers.IntegerField()
    bonus_discount_amount_BYN = serializers.DecimalField(max_digits=4, decimal_places=2)
    bonus_points = serializers.IntegerField()
    service_name = serializers.CharField(max_length=255)